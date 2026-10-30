// Sign-in option studies: shared intro controls and prototype sign-in.
// Every animated element rests in its final state; the intro only runs while <body> has .play.
// Skipping removes the animations, so the page snaps to that resting state.
(function () {
  const $ = (id) => document.getElementById(id);
  const body = document.body;
  const card = document.querySelector(".card");
  const skipBtn = $("skip");
  const PROTOTYPE = "https://callierae.github.io/CarrowmorePrototype/prototype/";
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  let playing = false;
  function finish() {
    playing = false;
    body.classList.add("skipped");
    skipBtn.hidden = true;
  }
  function play() {
    body.classList.remove("play", "skipped");
    void body.offsetWidth;            // restart every CSS animation from frame one
    if (reduced) { finish(); return; }
    body.classList.add("play");
    playing = true;
    skipBtn.hidden = false;
  }
  // The card's own entrance is the last beat of every intro.
  card.addEventListener("animationend", (e) => { if (e.target === card && playing) finish(); });

  skipBtn.addEventListener("click", finish);
  $("replay").addEventListener("click", (e) => { e.stopPropagation(); play(); });
  // Any key or tap during the intro skips to the sign-in, so nobody is held at the door.
  window.addEventListener("keydown", () => { if (playing) finish(); });
  window.addEventListener("pointerdown", (e) => {
    if (playing && !e.target.closest(".dock")) finish();
  });

  // ---------- prototype sign-in (mirrors prototype/index.html; not real security) ----------
  const tabs = { k: $("tab-k"), e: $("tab-e") };
  const forms = { k: $("form-k"), e: $("form-e") };
  const err = $("si-err");
  function pick(which) {
    for (const key of ["k", "e"]) {
      tabs[key].setAttribute("aria-selected", String(key === which));
      forms[key].hidden = key !== which;
    }
    err.textContent = "";
  }
  tabs.k.addEventListener("click", () => pick("k"));
  tabs.e.addEventListener("click", () => pick("e"));

  function signedIn(who) {
    $("signin-body").hidden = true;
    $("done-who").textContent = who;
    $("done").hidden = false;
    $("done-link").focus();
  }
  forms.k.addEventListener("submit", (e) => {
    e.preventDefault();
    const code = $("k-code").value.trim().toUpperCase();
    if (!/^K\d{4}$/.test(code)) { err.textContent = "Keeper codes are a K and four digits, for example K0566."; return; }
    if ($("k-pass").value !== "carrowmore") { err.textContent = "That password doesn't match. The prototype password for keepers is carrowmore."; return; }
    signedIn(code);
  });
  forms.e.addEventListener("submit", (e) => {
    e.preventDefault();
    const email = $("e-user").value.trim();
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { err.textContent = "Enter a work email, for example recruiter@carrowmore-array.example."; return; }
    if ($("e-pass").value !== "array") { err.textContent = "That password doesn't match. The prototype password for employers is array."; return; }
    signedIn(email);
  });
  $("done-link").href = PROTOTYPE;
  $("again").addEventListener("click", () => {
    $("done").hidden = true; $("signin-body").hidden = false;
    $("k-pass").value = ""; $("e-pass").value = ""; pick("k");
  });

  play();
})();
