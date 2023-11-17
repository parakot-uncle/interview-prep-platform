import ReactPlayer from "react-player";
import Image from "next/image";

function BodyDetections(props) {
  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold">Detected Gestures</h2>
      <ReactPlayer
        url={props?.attempt?.detected_video}
        width="100%"
        controls={true}
      />
      <h3 className="font-medium">Key Moments</h3>
      <div className="space-y-6">
        {props?.attempt?.body_detections?.map((detection, index) => {
          return (
            <div key={index} className="flex space-x-10 items-center">
              <img src={detection?.image} className="w-[60%]" />
              <p className="w-[40%]">{detection?.detection}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default BodyDetections;
