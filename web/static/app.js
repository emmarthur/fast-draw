const phaseText = document.getElementById("phase-text");
const actionBtn = document.getElementById("btn-action");
const resultText = document.getElementById("result-text");
const errorEl = document.getElementById("error-text");

/** @type {"idle"|"waiting"|"draw"|"result"} */
let phase = "idle";
let drawAt = 0;
let waitTimer = null;

function setError(message) {
  errorEl.hidden = !message;
  errorEl.textContent = message || "";
}

function setResult(message, outcome) {
  resultText.hidden = false;
  resultText.textContent = message;
  resultText.className = "result-text";
  if (outcome) resultText.classList.add(`is-${outcome}`);
}

function clearTimers() {
  if (waitTimer) {
    clearTimeout(waitTimer);
    waitTimer = null;
  }
}

async function evaluate(elapsedSec, early) {
  const res = await fetch("/api/evaluate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ elapsed_sec: elapsedSec, early }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || "Could not score round.");
  return data;
}

function beginWaiting() {
  phase = "waiting";
  resultText.hidden = true;
  actionBtn.disabled = true;
  actionBtn.hidden = true;
  phaseText.textContent = "It is high noon...";
  phaseText.className = "phase-text is-wait";
}

function showDraw() {
  phase = "draw";
  drawAt = performance.now();
  phaseText.textContent = "DRAW!";
  phaseText.className = "phase-text is-draw";
  actionBtn.hidden = false;
  actionBtn.disabled = false;
  actionBtn.textContent = "Draw!";
  actionBtn.focus();
}

async function onReact() {
  if (phase === "waiting") {
    clearTimers();
    phase = "result";
    actionBtn.hidden = true;
    try {
      const data = await evaluate(0, true);
      setResult(data.message, data.outcome);
    } catch (err) {
      setError(err.message);
    }
    phaseText.textContent = "Round over";
    phaseText.className = "phase-text";
    actionBtn.hidden = false;
    actionBtn.disabled = false;
    actionBtn.textContent = "Play again";
    phase = "idle";
    return;
  }

  if (phase !== "draw") return;

  const elapsed = (performance.now() - drawAt) / 1000;
  phase = "result";
  actionBtn.disabled = true;
  actionBtn.hidden = true;

  try {
    const data = await evaluate(elapsed, false);
    setResult(data.message, data.outcome);
  } catch (err) {
    setError(err.message);
  }

  phaseText.textContent = "Round over";
  phaseText.className = "phase-text";
  actionBtn.hidden = false;
  actionBtn.disabled = false;
  actionBtn.textContent = "Play again";
  phase = "idle";
}

async function startRound() {
  if (phase === "waiting" || phase === "draw") return;
  setError(null);
  resultText.hidden = true;
  clearTimers();
  beginWaiting();

  try {
    const res = await fetch("/api/wait");
    const { wait_sec } = await res.json();
    if (!res.ok) throw new Error("Could not start round.");
    waitTimer = setTimeout(() => {
      waitTimer = null;
      showDraw();
    }, wait_sec * 1000);
  } catch (err) {
    setError(err.message || "Could not start round.");
    phase = "idle";
    actionBtn.hidden = false;
    actionBtn.disabled = false;
    actionBtn.textContent = "Start round";
    phaseText.textContent = "Press start when you are ready.";
  }
}

actionBtn.addEventListener("click", () => {
  if (phase === "idle") startRound();
  else onReact();
});

document.addEventListener("keydown", (event) => {
  if (event.code !== "Space" && event.key !== " ") return;
  if (phase === "draw" || phase === "waiting") {
    event.preventDefault();
    onReact();
  }
});
