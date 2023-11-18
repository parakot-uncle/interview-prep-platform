import ReactPlayer from "react-player";
import Card from "../common/Card";
import ProgressBar from "@ramonak/react-progress-bar";

const positiveAudioEmotions = ["happy", "calm", "neutral"];
const negativeAudioEmotions = {
  sad: "sad",
  fear: "afraid",
  disgust: "annoyed",
};

const positiveGestureFeedback = {
  Appropriate:
    "You were looking into the camera - an ideal gestures during an interview.",
};
const negativeGestureFeedback = {
  Cheating: "Looking down during an interview gives an impression of cheating.",
  Disinterested:
    "Looking elsewhere during an interview may make you look disterested and give a bad impression to the interviewer.",
  Confused: "You looked confused and out of pace with the interview.",
};

function PreviousAttemptSummary(props) {
  const question = props?.question;
  const attempt = props?.attempt;

  const positiveFeedback = [];
  const negativeFeedback = [];

  let emotion = attempt?.emotion_detected_from_audio;
  let emotionIsPositive = true;
  if (negativeAudioEmotions[emotion]) {
    emotion = negativeAudioEmotions[emotion];
    emotionIsPositive = false;
  }

  const emotionFeedback = `You seemed to be ${emotion} during the interview.`;

  if (emotion) {
    if (emotionIsPositive) {
      positiveFeedback.push(
        emotionFeedback +
          " Not being stressed during an interview boosts overall confidence and impact of delivery."
      );
    } else {
      negativeFeedback.push(
        emotionFeedback +
          " Taking stress can affect delivery and reduce the chances of success."
      );
    }
  }

  attempt?.body_detections?.forEach((detection) => {
    const det = detection?.detection;
    if (positiveGestureFeedback[det]) {
      positiveFeedback.push(positiveGestureFeedback[det]);
    } else {
      negativeFeedback.push(negativeGestureFeedback[det]);
    }
  });

  if (props?.showSimilarityScore) {
    if (attempt?.answer_similarity_score > 50) {
      positiveFeedback.push(
        "Your answer matched the expectations. You have a good understanding of the concept in question."
      );
    } else {
      negativeFeedback.push(
        "Your answer was not upto the mark. You need to work on your concepts."
      );
    }
  }

  return (
    <>
      <ReactPlayer url={attempt?.video} width="100%" controls={true} />
      <div className="flex space-x-4 my-6">
        <Card className="bg-tertiaryGreen-100 text-tertiaryGreen-120 w-[50%] space-y-4 p-8">
          <h3 className="font-medium text-lg">Positives</h3>
          <ul className="list-disc px-4">
            {positiveFeedback?.map((feedback, index) => {
              return <li key={index}>{feedback}</li>;
            })}
          </ul>
        </Card>
        <Card className="bg-tertiaryRed-100 text-tertiaryRed-150 w-[50%] space-y-4 p-8">
          <h3 className="font-medium text-lg">Negatives</h3>
          <ul className="list-disc px-4">
            {negativeFeedback?.map((feedback, index) => {
              return <li key={index}>{feedback}</li>;
            })}
          </ul>
        </Card>
      </div>
      <div className="flex space-x-4 my-6">
        <Card className="bg-blackShade-50 w-[50%] space-y-4 p-8">
          <h3 className="font-medium text-lg">Your answer</h3>
          <p>{attempt?.user_answer}</p>
        </Card>
        <Card className="bg-blackShade-50 w-[50%] space-y-4 p-8">
          <h3 className="font-medium text-lg">{`${
            (props?.showSampleAnswer && "Sample") || "Suggested"
          } answer`}</h3>
          <p>{question?.answer}</p>
        </Card>
      </div>
      {props?.showSimilarityScore && (
        <div className="space-y-4">
          <h2 className="text-lg font-medium mb-4">
            Percentage matching expectations
          </h2>
          <ProgressBar
            completed={attempt?.answer_similarity_score?.toFixed(2)}
            bgColor="green"
          />
        </div>
      )}
      {props?.showAnswerTips && (
        <div className="flex space-x-4 my-6">
          <Card className="bg-blackShade-50 w-[50%] space-y-4 p-8">
            <h3 className="font-medium text-lg">Things to keep in mind</h3>
            <ul className="list-disc px-4">
              {question?.answer_guidelines?.map((guideline, index) => {
                return <li key={index}>{guideline}</li>;
              })}
            </ul>
          </Card>
          <Card className="bg-blackShade-50 w-[50%] space-y-4 p-8">
            <h3 className="font-medium text-lg">Some Answer Tips</h3>
            <ul className="list-disc px-4">
              {question?.answer_tips?.map((tip, index) => {
                return <li key={index}>{tip}</li>;
              })}
            </ul>
          </Card>
        </div>
      )}
    </>
  );
}

export default PreviousAttemptSummary;
