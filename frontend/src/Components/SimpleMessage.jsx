import { RiRobot2Line } from "react-icons/ri";
import PropTypes from "prop-types";

export const SimpleMessage = ({ children }) => {
  return (
    <div className="flex flex-row items-center gap-2 h-full">
      <RiRobot2Line size={18} className="text-blue-800" />
      <span className="bg-gray-200 p-2 w-[70%] animate__animated animate__faster animate__fadeIn  rounded-lg font-lora">
        {children}
      </span>
    </div>
  );
};

SimpleMessage.propTypes = {
  children: PropTypes.any,
};
