import SidePanel from "../common/SidePanel";

function QuestionsPanel(props) {
  return (
    // <SidePanel show={props?.show} onClose={props?.onClose} title="Questions">
    <div className="bg-[#292929] min-h-[93vh] overflow-y-auto flex-shrink-0">
      {props?.questions?.map((question, index) => {
        return (
          <button
            key={question?.id}
            className={`p-4 block`}
            style={{
              ...(props?.currentQuestion == index + 1 && {
                backgroundColor: "#5688d4",
              }),
            }}
            onClick={() => {
              props?.onChangeQuestion(index + 1);
            }}
          >
            {`Q.${index + 1}`}
          </button>
        );
      })}
    </div>
    // </SidePanel>
  );
}

export default QuestionsPanel;
