import React, { useCallback, useRef, useState } from "react";
import Webcam from "react-webcam";
import Card from "../common/Card";

function VideoRecorder(props) {
  const webcamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const [capturing, setCapturing] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);
  const [previewIsShown, setPreviewIsShown] = useState(true);

  const height = 400;
  const width = 600;

  const handleDataAvailable = useCallback(
    ({ data }) => {
      if (data.size > 0) {
        setRecordedChunks((prev) => prev.concat(data));
      }
    },
    [setRecordedChunks]
  );

  const handleStartCaptureClick = useCallback(() => {
    props?.onStartRecording();
    setRecordedChunks([]);
    setCapturing(true);
    mediaRecorderRef.current = new MediaRecorder(webcamRef.current.stream, {
      mimeType: "video/webm",
    });
    mediaRecorderRef.current.addEventListener(
      "dataavailable",
      handleDataAvailable
    );
    mediaRecorderRef.current.start();
  }, [webcamRef, setCapturing, mediaRecorderRef, handleDataAvailable]);

  const handleStopCaptureClick = useCallback(() => {
    props?.onStopRecording();
    mediaRecorderRef.current.stop();
    setCapturing(false);
  }, [mediaRecorderRef, setCapturing]);

  const handleDownload = useCallback(() => {
    if (recordedChunks.length) {
      const blob = new Blob(recordedChunks, {
        type: "video/webm",
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      document.body.appendChild(a);
      a.style = "display: none";
      a.href = url;
      a.download = "react-webcam-stream-capture.webm";
      a.click();
      window.URL.revokeObjectURL(url);
      setRecordedChunks([]);
    }
  }, [recordedChunks]);

  const videoConstraints = {
    width: width,
    height: height,
    facingMode: "user",
  };

  return (
    <div className="Container space-y-6">
      <Webcam
        height={height}
        width={width}
        audio={true}
        mirrored={false}
        ref={webcamRef}
        videoConstraints={videoConstraints}
        muted={true}
      />
      <div className="flex space-x-8">
        {capturing ? (
          <button
            className="text-sm rounded-md px-4 py-2 bg-red-600 hover:bg-red-400"
            onClick={handleStopCaptureClick}
          >
            Stop Recording
          </button>
        ) : (
          <button
            className="text-sm rounded-md px-4 py-2 bg-[#256bd4] hover:bg-tertiaryBlue-100"
            onClick={handleStartCaptureClick}
          >
            Start Recording
          </button>
        )}
        {recordedChunks.length > 0 && (
          <button
            onClick={handleDownload}
            className="text-sm rounded-md px-4 py-2 bg-[#256bd4] hover:bg-tertiaryBlue-100"
          >
            Download
          </button>
        )}
      </div>
    </div>
  );
}

export default VideoRecorder;
