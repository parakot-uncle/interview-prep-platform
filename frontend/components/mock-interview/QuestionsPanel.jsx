import SidePanel from "../common/SidePanel";

function QuestionsPanel(props) {
  const array = [];
  let div = parseInt(props?.currentQuestion / 10);
  if (props?.currentQuestion % 10 == 0) {
    div -= 1;
  }
  const num = div * 10;
  for (let i = 1; i <= 10; i += 1) {
    array.push(num + i);
  }

  return (
    // <SidePanel show={props?.show} onClose={props?.onClose} title="Questions">
    <div className="bg-[#292929] h-[93vh] flex-shrink-0 flex flex-col justify-center">
      {array?.map((num, index) => {
        return (
          <button
            key={index}
            className={`p-4 block w-full`}
            style={{
              ...(props?.currentQuestion == num && {
                backgroundColor: "#5688d4",
              }),
            }}
            onClick={() => {
              props?.onChangeQuestion(num);
            }}
          >
            {`Q.${num}`}
          </button>
        );
      })}
    </div>
    // </SidePanel>
  );
}

export default QuestionsPanel;
