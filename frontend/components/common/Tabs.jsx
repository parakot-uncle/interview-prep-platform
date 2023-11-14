function Tabs(props) {
  return (
    <div className="w-fit space-x-4 border-b-[1px]">
      {props?.tabs?.map((tab, index) => {
        return (
          <button
            key={index}
            onClick={() => {
              props?.onTabClick(tab);
            }}
            className={`${
              props?.currentTab == tab &&
              "font-medium text-tertiaryBlue-50 border-b-4 border-b-tertiaryBlue-50"
            } px-4 py-2`}
          >
            {tab}
          </button>
        );
      })}
    </div>
  );
}

export default Tabs;
