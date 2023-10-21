import { FaRobot } from "react-icons/fa";
import "../Styles/Chatbot.css";
import "animate.css";
import { useState } from "react";
import Chatbot from "./Chatbot";

export const ChatbotButton = () => {
  const [openChat, setOpenChat] = useState(false);
  return (
    <div>
      {!openChat ? (
        <>
          <div className="chatbot-btn-background chatbot-btn w-40 h-20 p-40 opacity-20 animate__animated animate__zoomIn  animate__infinite"></div>
          <button
            className="chatbot-btn relative "
            type="button"
            onClick={() => {
              setOpenChat(!openChat);
            }}
          >
            <FaRobot fontSize={20} />
            <span>Chat Bot</span>
          </button>
        </>
      ) : (
        <Chatbot open={openChat} set={setOpenChat} />
      )}
    </div>
  );
};
