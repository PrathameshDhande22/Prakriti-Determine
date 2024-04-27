import PropTypes from "prop-types";
import { RiRobot2Line } from "react-icons/ri";

export const QuestionMessage = ({ children }) => {
  return (
    <div className="flex flex-row items-center gap-2 h-full">
      <RiRobot2Line size={18} className="text-blue-800" />
      <div className="w-[70%] animate__animated animate__faster animate__fadeIn">
        {children}
      </div>
    </div>
  );
};

QuestionMessage.propTypes = {
  children: PropTypes.node,
};
