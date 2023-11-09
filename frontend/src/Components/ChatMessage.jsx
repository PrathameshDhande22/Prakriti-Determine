import PropTypes from "prop-types";
import { RiRobot2Line } from "react-icons/ri";
import parse from "html-react-parser";

export const ChatMessage = ({ message }) => {
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
};

ChatMessage.propTypes = {
  message: PropTypes.string,
};
