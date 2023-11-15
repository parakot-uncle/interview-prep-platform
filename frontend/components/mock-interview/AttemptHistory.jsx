import moment from "moment/moment";
import Card from "../common/Card";

function AttemptHistory(props) {
  const numberOfAttempts = props?.attempts?.length;
  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold">Attempt History</h2>
      <div className="space-y-4 h-[400px] overflow-y-auto">
        {props?.attempts?.map((attempt, index) => {
          return (
            <Card
              className={`${
                (attempt?._id == props?.currentAttemptId &&
                  "bg-tertiaryBlue-100") ||
                "bg-blackShade-50"
              } flex justify-between items-center cursor-pointer`}
              key={index}
              onClick={() => {
                props?.onAttemptClick(attempt?._id);
              }}
            >
              <p className="font-medium">{`Attempt ${
                numberOfAttempts - index
              }`}</p>
              <div className="flex space-x-6">
                <p>{moment(attempt?.date).format("ll")}</p>
                <p>{">"}</p>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

export default AttemptHistory;
