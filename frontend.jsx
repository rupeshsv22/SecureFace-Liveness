import { useRef, useState, useEffect } from "react";

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const wsRef = useRef(null);
  const intervalRef = useRef(null);

  const [result, setResult] = useState("Not Started");
  const [connected, setConnected] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  // =============================
  // Start Camera
  // =============================
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 },
      });

      videoRef.current.srcObject = stream;
      console.log("Camera started");
    } catch (err) {
      console.error("Camera error:", err);
      setResult("Camera access denied");
    }
  };

const createSession = async () => {
  const res = await fetch("http://127.0.0.1:8000/session/new");
  const data = await res.json();

  setSessionId(data.session_id);
  console.log("Session created:", data.session_id);
};
const resetSession = async () => {
  if (!sessionId) return;

  await fetch(`http://127.0.0.1:8000/session/reset/${sessionId}`, {
    method: "POST",
  });

  setResult("Session Reset");
};

  // =============================
  // Start WebSocket Liveness
  // =============================
  const startLiveness = () => {
    if (wsRef.current) {
      console.log("WebSocket already running");
      return;
    }

    if (!sessionId) {
    alert("Create session first");
    return;
    }

    const ws = new WebSocket(
    `ws://127.0.0.1:8000/ws/liveness/${sessionId}`
    );

    wsRef.current = ws;
    setProcessing(true);

    ws.onopen = () => {
      console.log("WebSocket connected");
      setConnected(true);
      startStreaming();
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      console.log("Server Response:", data);

      setResult(JSON.stringify(data, null, 2));

      if (data.liveness === true) {
        console.log("LIVE VERIFIED");
        stopStreaming();
        setResult("✅ LIVE VERIFIED");
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setResult("WebSocket error");
      stopStreaming();
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
      setConnected(false);
      wsRef.current = null;
    };
  };

  // =============================
  // Send Frames Every 300ms
  // =============================
  const startStreaming = () => {
    intervalRef.current = setInterval(() => {
      sendFrame();
    }, 80);
  };

  const stopStreaming = () => {
    clearInterval(intervalRef.current);

    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    setConnected(false);
    setProcessing(false);
  };

  // =============================
  // Capture Frame & Send
  // =============================
  const sendFrame = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;

    if (!video || video.readyState !== 4) {
      console.log("Video not ready");
      return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    const base64 = canvas.toDataURL("image/jpeg", 0.7);
    const base64Data = base64.split(",")[1];

    if (wsRef.current && wsRef.current.readyState === 1) {
      console.log("Sending frame...");
      wsRef.current.send(base64Data);
    }
  };

  // =============================
  // Cleanup on Unmount
  // =============================
  useEffect(() => {
    return () => {
      stopStreaming();
      if (videoRef.current?.srcObject) {
        videoRef.current.srcObject.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>Enterprise KYC Face Liveness</h2>

      <video
        ref={videoRef}
        autoPlay
        playsInline
        width="420"
        style={{
          borderRadius: "12px",
          border: "3px solid #222",
          marginBottom: "20px",
        }}
      />

      <canvas ref={canvasRef} style={{ display: "none" }} />

      <br />

      <button onClick={createSession}>
      🆕 Create Session
      </button>

      <button onClick={resetSession}>
      🔄 Reset Session
      </button>

      <button onClick={startCamera} disabled={processing}>
        🎥 Start Camera
      </button>

      <button onClick={startLiveness} disabled={processing}>
        🔐 Start Liveness Check
      </button>

      <h3>Result:</h3>
      <pre
        style={{
          background: "#111",
          color: "#0f0",
          padding: "10px",
          borderRadius: "8px",
          maxWidth: "500px",
          margin: "auto",
        }}
      >
        {result}
      </pre>
    </div>
  );
}

export default App;
