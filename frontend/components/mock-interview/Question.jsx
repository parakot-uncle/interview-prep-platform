import Card from "../common/Card";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faClock } from "@fortawesome/free-solid-svg-icons";

function Question(props) {
  return (
    <>
      <Card backgroundColor={"#242424"} className="w-full space-y-2 p-6">
        <h2 className="text-xl font-semibold">{`Question ${props?.currentQuestion}`}</h2>
        <div className="text-md">{props?.question?.question}</div>
      </Card>
      <Card backgroundColor={"#242424"} className="w-full p-6">
        <h3 className="text-lg font-medium">Some instructions</h3>
        <div className="text-md flex space-x-2 items-center my-4">
          <FontAwesomeIcon icon={faClock} />
          <p>5 mins</p>
        </div>
        <div>
          <h4 className="font-medium">Be Yourself</h4>
          <p>
            Just like an in-person or phone interview, this is your chance to
            shine and share what you offer. Be authentic and remember—relax!
            Have fun and let your skills and personality do the talking! Most
            importantly, be authentic. Just speak and focus in the way that
            makes you comfortable.
          </p>
        </div>
      </Card>
    </>
  );
}

export default Question;
