import PropTypes from "prop-types";
import { RiRobot2Line } from "react-icons/ri";
import parse from "html-react-parser";

export const ChatMessage = ({ message }) => {
  if (typeof message === "string") {
    return (
      <>
        <div className="flex flex-row items-center gap-2 h-full">
          <RiRobot2Line size={18} className="text-blue-800" />
          <span className="bg-gray-200 p-2 w-[70%]  rounded-lg font-lora select-none">
            {parse(message)}
          </span>
        </div>
      </>
    );
  } else if (typeof message === "object") {
    const len = Object.keys(message["options"]).length;
    if (len === 2) {
      return (
        <>
          <div className="flex flex-row items-center gap-2 h-full">
            <RiRobot2Line size={18} className="text-blue-800" />
            <div className="w-[70%]">
              <div className="bg-gray-200 p-2 w-full  rounded-lg font-lora select-none">
                {message["question"]}
              </div>
              <div className="w-full pt-1 flex flex-row gap-1 justify-between items-center">
                {Object.keys(message?.options).map((objkey, index) => {
                  return (
                    <button
                      type="button"
                      className="font-lora capitalize border-2 border-gray-400 rounded-md w-1/2 py-1 shadow-lg"
                      key={index}
                    >
                      {String(message?.options[objkey])}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        </>
      );
    } else if (len === 3)
      return (
        <>
          <div className="flex flex-row items-center gap-2 h-full">
            <RiRobot2Line size={18} className="text-blue-800" />
            <div className="w-[70%]">
              <div className="bg-gray-200 p-2 w-full rounded-lg font-lora select-none">
                {message["question"]}
              </div>
              <div className="w-full pt-1 flex flex-col flex-wrap gap-1 items-center">
                {Object.keys(message?.options).map((objkey, index) => {
                  return (
                    <button
                      name={objkey}
                      type="button"
                      className="font-lora capitalize border-2 border-gray-400 rounded-md w-full py-1 shadow-md"
                      key={index}
                    >
                      {String(message?.options[objkey])}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        </>
      );
  }
};

ChatMessage.propTypes = {
  message: PropTypes.any,
};
