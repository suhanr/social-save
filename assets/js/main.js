(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");

  /* Header: shadow on scroll */
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* Mobile menu */
  var toggle = document.querySelector(".nav-toggle");
  var panel = document.getElementById("mobile-panel");
  function setMenu(open) {
    if (!toggle || !panel) return;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    panel.classList.toggle("is-open", open);
  }
  if (toggle && panel) {
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && panel.classList.contains("is-open")) {
        setMenu(false);
        toggle.focus();
      }
    });
    document.addEventListener("click", function (e) {
      if (panel.classList.contains("is-open") && !panel.contains(e.target) && !toggle.contains(e.target)) setMenu(false);
    });
    window.matchMedia("(min-width: 900px)").addEventListener("change", function (m) {
      if (m.matches) setMenu(false);
    });
  }

  /* Scroll reveal */
  var items = [].slice.call(document.querySelectorAll(".reveal"));
  if ("IntersectionObserver" in window && items.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          // Also reveal anything already above the viewport (anchor jumps, restored scroll).
          if (en.isIntersecting || en.boundingClientRect.top < 0) {
            en.target.classList.add("in");
            io.unobserve(en.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  /* Table of contents: highlight current section */
  var tocLinks = [].slice.call(document.querySelectorAll(".toc a"));
  if ("IntersectionObserver" in window && tocLinks.length) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var spy = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting && map[en.target.id]) {
            tocLinks.forEach(function (a) { a.classList.remove("is-active"); });
            map[en.target.id].classList.add("is-active");
          }
        });
      },
      { rootMargin: "-20% 0px -70% 0px" }
    );
    Object.keys(map).forEach(function (id) {
      var h = document.getElementById(id);
      if (h) spy.observe(h);
    });
  }

  /* Link form */
  var PLATFORMS = [
    { id: "Instagram", hosts: ["instagram.com"] },
    { id: "Facebook", hosts: ["facebook.com", "fb.watch", "fb.com"] },
    { id: "TikTok", hosts: ["tiktok.com"] },
    { id: "YouTube", hosts: ["youtube.com", "youtu.be"] }
  ];
  function detect(host) {
    host = host.toLowerCase().replace(/^www\./, "");
    for (var i = 0; i < PLATFORMS.length; i++) {
      for (var j = 0; j < PLATFORMS[i].hosts.length; j++) {
        var h = PLATFORMS[i].hosts[j];
        if (host === h || host.slice(-(h.length + 1)) === "." + h) return PLATFORMS[i].id;
      }
    }
    return null;
  }
  function esc(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  var ICONS = {
    error: '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>',
    ok: '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>'
  };

  [].forEach.call(document.querySelectorAll("form.link-form"), function (form) {
    var input = form.querySelector("input[name=u]");
    var field = form.querySelector(".link-field");
    var status = form.querySelector(".form-status");
    var paste = form.querySelector(".paste-btn");
    var only = form.getAttribute("data-only"); // e.g. "YouTube"
    var badge = form.getAttribute("data-badge") || "";
    var other = form.getAttribute("data-other") || "";
    var live = form.hasAttribute("data-live"); // validate in page instead of navigating

    function show(kind, html) {
      field.classList.toggle("is-invalid", kind === "error");
      input.setAttribute("aria-invalid", kind === "error" ? "true" : "false");
      status.innerHTML = html ? '<div class="notice notice-' + kind + '">' + (ICONS[kind] || "") + "<div>" + html + "</div></div>" : "";
    }
    function check() {
      var v = input.value.trim();
      if (!v) return show("error", "Paste a link to get started.") || false;
      var url;
      try {
        url = new URL(/^[a-z][a-z0-9+.-]*:\/\//i.test(v) ? v : "https://" + v);
      } catch (err) {
        return show("error", "That doesn’t look like a valid link. Check it and try again.") || false;
      }
      if (!/^https?:$/.test(url.protocol) || url.hostname.indexOf(".") < 0) {
        return show("error", "That doesn’t look like a valid link. Check it and try again.") || false;
      }
      var p = detect(url.hostname);
      if (only && p !== only) {
        return show("error", "This tool works with " + esc(only) + " links." + (other ? ' For other platforms, use the <a href="' + esc(other) + '">Social Media downloader</a>.' : "")) || false;
      }
      if (!p) {
        return show("error", "This link isn’t from a supported platform. Try an Instagram, Facebook, TikTok or YouTube link.") || false;
      }
      show(
        "ok",
        "<strong>" + esc(p) + " link detected.</strong> Online downloads aren’t available on this website yet. Get the Social Save Android app to save this media." +
          (badge ? '<div class="notice-actions"><a class="play-badge" href="' + esc(badge) + '"><img src="' + esc(form.getAttribute("data-badge-img")) + '" alt="Get it on Google Play" width="162" height="48"></a></div>' : "")
      );
      return true;
    }

    if (live) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        check();
        input.focus();
      });
      input.addEventListener("input", function () {
        if (field.classList.contains("is-invalid")) show("", "");
      });
      var qs = new URLSearchParams(location.search).get("u");
      if (qs) {
        input.value = qs;
        check();
      }
    } else {
      form.addEventListener("submit", function (e) {
        if (!input.value.trim()) {
          e.preventDefault();
          show("error", "Paste a link to get started.");
          input.focus();
        }
      });
    }

    if (paste && navigator.clipboard && navigator.clipboard.readText && window.isSecureContext) {
      paste.classList.add("is-available");
      paste.addEventListener("click", function () {
        navigator.clipboard.readText().then(
          function (t) {
            if (t) {
              input.value = t.trim();
              input.focus();
              if (live) check();
            }
          },
          function () { input.focus(); }
        );
      });
    }
  });
})();
