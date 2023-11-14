import ReactPlayer from "react-player";
import Card from "../common/Card";
import ProgressBar from "@ramonak/react-progress-bar";

function PreviousAttemptSummary(props) {
  return (
    <>
      <ReactPlayer url={props?.attempt?.video} width="100%" controls={true} />
      <div className="flex space-x-4 my-6">
        <Card className="bg-tertiaryGreen-100 text-tertiaryGreen-120 w-[50%] space-y-4 p-6">
          <h3 className="font-medium text-lg">Positives</h3>
          <p>
            Clarity in Responses: Your responses were clear and articulate,
            demonstrating a strong understanding of the questions asked.
            Thoughtful Approach: I appreciated how you approached each question
            thoughtfully, showcasing a well-rounded perspective on the topics
            discussed. Adaptability: Your ability to adapt to the AI interview
            format was impressive, reflecting your comfort with technology and
            communication skills. Confidence and Poise: Your confident demeanor
            throughout the interview conveyed professionalism and assurance in
            your knowledge.
          </p>
        </Card>
        <Card className="bg-tertiaryRed-100 text-tertiaryRed-150 w-[50%] space-y-4 p-6">
          <h3 className="font-medium text-lg">Negatives</h3>
          <p>
            Clarity in Responses: Your responses were clear and articulate,
            demonstrating a strong understanding of the questions asked.
            Thoughtful Approach: I appreciated how you approached each question
            thoughtfully, showcasing a well-rounded perspective on the topics
            discussed. Adaptability: Your ability to adapt to the AI interview
            format was impressive, reflecting your comfort with technology and
            communication skills. Confidence and Poise: Your confident demeanor
            throughout the interview conveyed professionalism and assurance in
            your knowledge.
          </p>
        </Card>
      </div>
      <div className="flex space-x-4 my-6">
        <Card className="bg-blackShade-50 w-[50%] space-y-4 p-6">
          <h3 className="font-medium text-lg">Your answer</h3>
          <p>
            Clarity in Responses: Your responses were clear and articulate,
            demonstrating a strong understanding of the questions asked.
            Thoughtful Approach: I appreciated how you approached each question
            thoughtfully, showcasing a well-rounded perspective on the topics
            discussed. Adaptability: Your ability to adapt to the AI interview
            format was impressive, reflecting your comfort with technology and
            communication skills. Confidence and Poise: Your confident demeanor
            throughout the interview conveyed professionalism and assurance in
            your knowledge.
          </p>
        </Card>
        <Card className="bg-blackShade-50 w-[50%] space-y-4 p-6">
          <h3 className="font-medium text-lg">Suggested answer</h3>
          <p>
            Clarity in Responses: Your responses were clear and articulate,
            demonstrating a strong understanding of the questions asked.
            Thoughtful Approach: I appreciated how you approached each question
            thoughtfully, showcasing a well-rounded perspective on the topics
            discussed. Adaptability: Your ability to adapt to the AI interview
            format was impressive, reflecting your comfort with technology and
            communication skills. Confidence and Poise: Your confident demeanor
            throughout the interview conveyed professionalism and assurance in
            your knowledge.
          </p>
        </Card>
      </div>
      <div className="space-y-4">
        <h2 className="text-lg font-medium mb-4">
          Percentage matching expectations
        </h2>
        <ProgressBar completed={60} bgColor="green" />
      </div>
    </>
  );
}

export default PreviousAttemptSummary;
