import moment from "moment/moment";
import Card from "../common/Card";

function AttemptHistory(props) {
  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold">Attempt History</h2>
      <div className="space-y-4">
        {props?.attempts?.map((attempt, index) => {
          return (
            <Card
              className={`${
                (attempt?.id == props?.currentAttemptId &&
                  "bg-tertiaryBlue-100") ||
                "bg-blackShade-50"
              } flex justify-between items-center cursor-pointer`}
              key={index}
              onClick={() => {
                props?.onAttemptClick(attempt?.id);
              }}
            >
              <p className="font-medium">{`Attempt ${index + 1}`}</p>
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
