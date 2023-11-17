import { Dialog, Transition } from "@headlessui/react";
import CloseIcon from "@/public/icons/CloseIcon";
import { Fragment, useEffect, useState } from "react";

function SidePanel(props) {
  const [showSidePanel, setShowSidePanel] = useState(false);

  const closeSidePanelHandler = () => {
    setShowSidePanel(false);
    props?.onClose();
  };

  useEffect(() => {
    setShowSidePanel(props?.show);
  }, [props?.show]);

  return (
    <Transition.Root show={showSidePanel} as={Fragment}>
      <Dialog
        as="div"
        className="fixed inset-0 z-10 lg:z-30 overflow-y-auto"
        onClose={closeSidePanelHandler}
      >
        <div className="absolute inset-0 overflow-hidden">
          <Transition.Child
            as={Fragment}
            enter="ease-in-out duration-500"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in-out duration-500"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <Dialog.Overlay className="absolute inset-0 bg-black bg-opacity-50 transition-opacity " />
          </Transition.Child>
          <div className="fixed inset-y-0 left-0 mt-16 lg:mt-0">
            <Transition.Child
              as={Fragment}
              enter="transform transition ease-in-out duration-500 sm:duration-700"
              enterFrom="-translate-x-full" // Start from the left (off-screen)
              enterTo="translate-x-0" // Move to the right (initial position)
              leave="transition ease-in-out duration-300 transform"
              leaveFrom="translate-x-0" // Start from the right (current position)
              leaveTo="-translate-x-full"
            >
              <div className="relative w-screen lg:max-w-lg">
                <div
                  className={`h-screen flex flex-col shadow-xl bg-[#292929]`}
                >
                  <div className="relative flex-1">
                    <div className="flex justify-between w-full my-4 px-4">
                      <div className="">
                        <p className="font-display font-medium text-sm lg:text-lg text-blackShade-50 flex-1">
                          {props?.title}
                        </p>
                      </div>
                      <div className=" ">
                        <button
                          className="rounded-full transition-colors hover:bg-tertiary-300 active:bg-tertiary-325 ml-auto p-2"
                          onClick={closeSidePanelHandler}
                        >
                          <CloseIcon height="19" width="19" />
                        </button>
                      </div>
                    </div>
                    <div>{props?.children}</div>
                  </div>
                </div>
              </div>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  );
}

export default SidePanel;
