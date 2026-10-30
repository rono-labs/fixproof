(function () {
  "use strict";
  var SC = window.SCENARIOS || [];
  var LIB = window.LIBRARY || [];
  var AGENTS = {
    "photo-agent": ["#b45309", "#fef0d6"],
    "file-agent": ["#1d4ed8", "#e1ebff"],
    "document-agent": ["#7c3aed", "#eee6ff"],
    "knowledge-agent": ["#0e7490", "#dcf3f8"]
  };
  var PHOTOS = {};
  var state = { sc: null, shown: 0, timer: null };
  var $ = function (id) { return document.getElementById(id); };
  var chat = $("chat");

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function cap(s) { return s ? s.charAt(0).toUpperCase() + s.slice(1) : s; }

  // text with library paths wrapped in <code>
  function rich(parent, text) {
    var rest = text;
    var paths = LIB.slice().sort(function (a, b) { return b.length - a.length; });
    while (rest.length) {
      var best = -1, bp = null;
      for (var i = 0; i < paths.length; i++) {
        var ix = rest.indexOf(paths[i]);
        if (ix >= 0 && (best < 0 || ix < best)) { best = ix; bp = paths[i]; }
      }
      if (best < 0) { parent.appendChild(document.createTextNode(rest)); break; }
      if (best > 0) parent.appendChild(document.createTextNode(rest.slice(0, best)));
      parent.appendChild(el("code", "path mono", bp));
      rest = rest.slice(best + bp.length);
    }
    return parent;
  }

  // ---- library tree
  function buildTree() {
    var t = $("tree");
    t.textContent = "";
    var last = [];
    LIB.forEach(function (p, idx) {
      var parts = p.split("/");
      var dirs = parts.slice(0, -1);
      for (var d = 0; d < dirs.length; d++) {
        if (last[d] !== dirs[d] || last.slice(0, d).join("/") !== dirs.slice(0, d).join("/")) {
          var dd = el("div", "dir d" + d, dirs[d] + "/");
          dd.style.paddingLeft = d * 14 + "px";
          t.appendChild(dd);
          last = dirs.slice(0, d + 1);
        }
      }
      last = dirs;
      var f = el("div", "file", parts[parts.length - 1]);
      f.style.marginLeft = dirs.length * 14 + "px";
      f.dataset.path = p;
      f.id = "f" + idx;
      t.appendChild(f);
    });
  }
  function lightTree() {
    var seen = {}, now = {};
    if (state.sc) {
      for (var i = 0; i < state.shown; i++) {
        state.sc.steps[i].files.forEach(function (f) {
          if (i === state.shown - 1) now[f] = true; else seen[f] = true;
        });
      }
    }
    var first = null;
    Array.prototype.forEach.call($("tree").querySelectorAll(".file"), function (n) {
      var p = n.dataset.path;
      n.classList.toggle("now", !!now[p]);
      n.classList.toggle("seen", !now[p] && !!(seen[p] || now[p]));
      if (now[p] && !first) first = n;
    });
    if (first && first.scrollIntoView) {
      var tr = $("tree"), r = first.getBoundingClientRect(), tb = tr.getBoundingClientRect();
      if (r.top < tb.top || r.bottom > tb.bottom) tr.scrollTop += r.top - tb.top - 60;
    }
  }

  // ---- step cards
  function stepCard(sc, i) {
    var s = sc.steps[i];
    var col = AGENTS[s.agent] || ["#444", "#eee"];
    var c = el("article", "card");
    c.dataset.step = String(i + 1);
    c.style.setProperty("--c", col[0]);
    c.style.setProperty("--bg-c", col[1]);
    var h = el("header");
    h.appendChild(el("span", "chip", s.agent));
    h.appendChild(el("span", "stepno", "Step " + (i + 1) + " of " + sc.steps.length));
    c.appendChild(h);
    c.appendChild(el("div", "lab", "Asked"));
    c.appendChild(rich(el("p", "ask"), s.ask));
    c.appendChild(el("div", "lab", "Found"));
    var ul = el("ul", "found");
    s.result.forEach(function (r) { ul.appendChild(rich(el("li"), r)); });
    c.appendChild(ul);
    var imgs = s.files.filter(function (f) { return PHOTOS[f]; });
    if (imgs.length) {
      var th = el("div", "thumbs");
      imgs.forEach(function (f) {
        var fig = el("figure");
        var im = el("img");
        im.src = "assets/" + f;
        im.alt = "Photo " + f.split("/").pop();
        fig.appendChild(im);
        fig.appendChild(el("figcaption", "mono", f.split("/").pop()));
        th.appendChild(fig);
      });
      c.appendChild(th);
    }
    if (s.parent) {
      var d = el("p", "decision");
      d.appendChild(el("b", null, "Decision: "));
      d.appendChild(document.createTextNode(cap(s.parent)));
      c.appendChild(d);
    }
    if (s.draft) {
      var dt = el("details", "draft");
      dt.open = true;
      dt.appendChild(el("summary", null, "Claim draft composed after this step"));
      dt.appendChild(el("pre", "mono", s.draft));
      c.appendChild(dt);
    }
    return c;
  }

  // ---- final answer
  var KEYS = ["Safety first", "Product", "Coverage", "Try this", "Claim", "Evidence", "Notes"];
  function parseAnswer(text) {
    var blocks = [], cur = null;
    text.split("\n").forEach(function (ln) {
      if (!ln.trim()) return;
      if (/^\s/.test(ln)) {
        if (cur) cur.lines.push(ln.trim());
        return;
      }
      var m = ln.match(/^(Safety first|Product|Coverage|Try this|Claim|Evidence|Notes)(\s*\(([^)]*)\))?:\s*(.*)$/);
      if (m) { cur = { label: m[1], sub: m[3] || "", rest: m[4], lines: [] }; }
      else {
        var g = ln.match(/^(.*):$/);
        if (g) cur = { label: g[1], sub: "", rest: "", lines: [], group: true };
        else cur = { label: "", sub: "", rest: ln, lines: [], plain: true };
      }
      blocks.push(cur);
    });
    return blocks;
  }
  function listFrom(lines, ordered) {
    var wrap = el("div");
    var list = null, kind = null;
    lines.forEach(function (ln) {
      var num = ln.match(/^\d+\.\s+(.*)$/), bul = ln.match(/^-\s+(.*)$/);
      if (num || bul) {
        var k = num ? "ol" : "ul";
        if (kind !== k) { list = el(k); wrap.appendChild(list); kind = k; }
        var li = el("li");
        var body = (num || bul)[1];
        var dm = body.match(/^(\d{4}-\d{2}-\d{2}): (.*)$/);
        if (dm) { li.appendChild(el("span", "when", dm[1])); body = dm[2]; list.className = "cal"; }
        var em = body.match(/^([^:]+\.(?:pdf|jpg)): (.*)$/);
        if (em && LIB.indexOf(em[1]) >= 0) {
          li.appendChild(el("code", "path mono", em[1]));
          li.appendChild(document.createTextNode(": "));
          body = em[2];
        }
        rich(li, body);
        list.appendChild(li);
      } else {
        kind = null;
        wrap.appendChild(rich(el("p"), ln));
      }
    });
    return wrap;
  }
  function answerCard(sc) {
    var card = el("section", "answer");
    card.id = "answer";
    card.dataset.step = "answer";
    card.appendChild(el("h3", null, "Uliya's answer"));
    var blocks = parseAnswer(sc.answer);
    var prod = null, cov = null;
    blocks.forEach(function (b) { if (b.label === "Product") prod = b; if (b.label === "Coverage") cov = b; });
    if (prod || cov) {
      var hero = el("div", "hero");
      if (cov) {
        var vm = cov.rest.match(/^(Not covered|Covered|Unclear)\b\.?\s*(.*)$/);
        if (vm) {
          var cls = vm[1].toLowerCase().replace(" ", "-");
          var pill = el("span", "pill " + cls, vm[1]);
          pill.id = "verdict";
          hero.appendChild(pill);
        }
      }
      if (prod) hero.appendChild(el("span", "prod", prod.rest));
      if (cov) {
        var why = cov.rest.replace(/^(Not covered|Covered|Unclear)\b\.?\s*/, "");
        hero.appendChild(rich(el("span", "why"), why));
      }
      card.appendChild(hero);
    }
    blocks.forEach(function (b) {
      if (b === prod || b === cov) return;
      if (b.plain) {
        if (/\?$/.test(b.rest)) {
          var q = el("div", "sec ask"); q.appendChild(el("p", null, b.rest)); card.appendChild(q);
        } else if (blocks.indexOf(b) === 0) {
          var t = el("h3", null, b.rest); t.style.marginTop = "0"; t.style.textTransform = "none"; t.style.fontSize = "19px"; t.style.color = "#17231f";
          card.appendChild(t);
        } else {
          var pp = el("div", "sec notes"); pp.appendChild(rich(el("p"), b.rest)); card.appendChild(pp);
        }
        return;
      }
      var cls2 = "sec" + (b.label === "Safety first" ? " safety" : "") + (b.label === "Notes" ? " notes" : "");
      var sec = el("div", cls2);
      var label = b.label, extra = "";
      var vm2 = label.match(/^(.*?)\s*\((.*)\)$/);
      if (b.group && vm2) { label = vm2[1]; extra = vm2[2]; }
      var h4 = el("h4", null, label + (b.sub ? " (" + b.sub + ")" : ""));
      sec.appendChild(h4);
      var money = extra.match(/\$[\d,]+/);
      if (money) {
        var st = el("div"); st.appendChild(el("span", "stat", money[0]));
        st.appendChild(document.createTextNode("of purchase value loses cover"));
        sec.appendChild(st);
      }
      if (b.rest) sec.appendChild(rich(el("p"), b.rest));
      if (b.lines.length) sec.appendChild(listFrom(b.lines));
      card.appendChild(sec);
    });
    return card;
  }
  function statusLine(sc) {
    var s = el("div", "statusline");
    s.id = "status";
    var label = { completed: "Completed", waiting_approval: "Waiting for your approval" }[sc.status] || sc.status;
    s.appendChild(el("span", "st " + sc.status, label));
    var tail = "";
    if (sc.saved) tail = "Saved to " + sc.saved + ". ";
    else if (sc.status === "waiting_approval") tail = "Nothing saved yet. ";
    tail += sc.delegations + " delegations (" + sc.delegation_detail + ").";
    s.appendChild(rich(el("span"), tail));
    return s;
  }
  function bubble(text, who) {
    var b = el("div", "bubble user");
    b.appendChild(el("span", "who", who));
    b.appendChild(document.createTextNode(text));
    return b;
  }

  // ---- reveal logic. units: step 0..n-1, then n = answer
  function total(sc) { return sc.steps.length + 1; }
  function addUnit(u) {
    var sc = state.sc, n = sc.steps.length, node;
    if (u < n) {
      if (sc.second_turn && sc.second_turn_before_step === u) {
        var sb = bubble(sc.second_turn, "You, reply");
        sb.id = "second-turn";
        chat.appendChild(sb);
      }
      node = stepCard(sc, u);
      chat.appendChild(node);
    } else {
      node = answerCard(sc);
      chat.appendChild(node);
      chat.appendChild(statusLine(sc));
    }
    return node;
  }
  function updateUi() {
    var sc = state.sc, n = sc.steps.length;
    var cur = Math.min(state.shown, n);
    $("counter").textContent = "Step " + cur + " of " + n + (state.shown > n ? " (answer)" : "");
    $("next").disabled = state.shown >= total(sc);
    if (state.shown >= total(sc)) stop();
    lightTree();
  }
  function next() {
    if (state.shown >= total(state.sc)) return;
    var node = addUnit(state.shown);
    state.shown++;
    updateUi();
    node.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
  function stop() {
    if (state.timer) { clearInterval(state.timer); state.timer = null; }
    $("play").textContent = "Play";
  }
  function play() {
    if (state.timer) { stop(); return; }
    if (state.shown >= total(state.sc)) return;
    $("play").textContent = "Pause";
    next();
    state.timer = setInterval(next, 1600);
  }
  function load(id, all) {
    stop();
    var sc = SC.filter(function (s) { return s.id === id; })[0] || SC[0];
    state.sc = sc;
    state.shown = 0;
    chat.textContent = "";
    Array.prototype.forEach.call(document.querySelectorAll(".tab"), function (t) {
      t.classList.toggle("active", t.dataset.s === sc.id);
    });
    chat.appendChild(bubble(sc.prompt, "You"));
    var it = el("p", "intake");
    it.textContent = "How the Skill reads it: " + sc.intake;
    chat.appendChild(it);
    if (all) {
      for (var u = 0; u < total(sc); u++) { addUnit(u); }
      state.shown = total(sc);
      chat.style.scrollBehavior = "auto";
      chat.scrollTop = 0;
      chat.style.scrollBehavior = "";
    }
    updateUi();
  }

  function init() {
    SC.forEach(function (s) {
      s.steps.forEach(function (st) {
        st.files.forEach(function (f) { if (/\.jpg$/i.test(f)) PHOTOS[f] = true; });
      });
      var t = $("tab-" + s.id);
      t.textContent = "";
      t.appendChild(el("span", "k", s.id));
      t.appendChild(document.createTextNode(s.title));
      t.addEventListener("click", function () { load(s.id, false); });
    });
    buildTree();
    $("next").addEventListener("click", next);
    $("play").addEventListener("click", play);
    $("reset").addEventListener("click", function () { load(state.sc.id, false); });
    var q = new URLSearchParams(location.search);
    var id = (q.get("s") || "A").toUpperCase();
    var step = q.get("step");
    load(id, step === "all");
    if (step && step !== "all") {
      var k = parseInt(step, 10) || 0;
      chat.style.scrollBehavior = "auto";
      for (var i = 0; i < k; i++) next();
      chat.style.scrollBehavior = "";
    }
  }
  init();
})();
