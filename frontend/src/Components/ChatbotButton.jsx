import { FaRobot } from "react-icons/fa";
import "../Styles/Chatbot.css";
import "animate.css";
import { useContext } from "react";
import Chatbot from "./Chatbot";
import { ChatbotOpen } from "./ChatbotOpen";

export const ChatbotButton = () => {
  const { open, setOpen } = useContext(ChatbotOpen);
  return (
    <div className="">
      {!open ? (
        <>
          <div className="chatbot-btn-background chatbot-btn w-40 h-20 p-40 opacity-20 animate__animated animate__zoomIn  animate__infinite"></div>
          <button
            className="chatbot-btn"
            type="button"
            onClick={() => {
              setOpen(!open);
            }}
          >
            <FaRobot fontSize={20} />
            <span>Chat Bot</span>
          </button>
        </>
      ) : (
        <Chatbot open={open} set={setOpen} />
      )}
    </div>
  );
};
