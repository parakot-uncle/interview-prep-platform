import { CountdownCircleTimer } from "react-countdown-circle-timer";
import ProgressTimer from "react-progress-bar-timer";

function Timer(props) {
  return (
    // <CountdownCircleTimer
    //   isPlaying={props?.timerIsRunning}
    //   duration={180}
    //   colors={["#004777", "#F7B801", "#A30000", "#A30000"]}
    //   colorsTime={[7, 5, 2, 0]}
    //   onComplete={props?.onTimerCompletion}
    //   size={props?.size}
    // >
    //   {({ remainingTime }) => {
    //     const minutes = Math.floor(remainingTime / 60);
    //     const seconds = remainingTime % 60;

    //     return `${minutes} mins : ${seconds} secs`;
    //   }}
    // </CountdownCircleTimer>
    <ProgressTimer
      direction="left"
      duration={props?.duration}
      started={props?.timerIsRunning}
      showDuration={true}
      fontSize={10}
      onFinish={props?.onTimerCompletion}
      variant="empty"
    />
  );
}

export default Timer;
