import PropTypes from "prop-types";
import { AiOutlineCaretRight } from "react-icons/ai";

const UserMessage = ({ message }) => {
  return (
    <div className="flex text-white items-center gap-0 flex-row w-fit self-end font-lora">
      <span className=" bg-blue-600 p-2 rounded-lg">{message}</span>
      <AiOutlineCaretRight color="blue" size={20} className=""/>
    </div>
  );
};
export default UserMessage;

UserMessage.propTypes = {
  message: PropTypes.string,
};
