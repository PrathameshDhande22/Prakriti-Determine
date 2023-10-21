import PropTypes from "prop-types";
import { useState } from "react";
import { IoSend, IoCloseSharp } from "react-icons/io5";
import "animate.css";
import { FiMaximize2 } from "react-icons/fi";
import { DeepChat } from "deep-chat-react";

const Chatbot = ({ open, set }) => {
  // const [queries, setQueries] = useState("");
  const [fullsize, setFullSize] = useState(false);
  return (
    <div className="h-full">
      <div
        className={`z-30  rounded-lg border-4 border-blue-400  pb-5 bg-white animate__animated animate__fadeIn ${
          fullsize ? "w-full h-screen top-0 absolute" : "fixed top-1/4 right-7"
        }`}
      >
        <div className="bg-sky-500 text-white px-3 py-2 flex flex-row justify-between text-lg font-serif">
          <span>AyurBot</span>
          <div className="space-x-3">
            <button
              type="button"
              className="hover:bg-sky-400"
              onClick={() => {
                setFullSize(!fullsize);
              }}
            >
              <FiMaximize2 />
            </button>
            <button
              className="hover:bg-sky-400"
              type="button"
              onClick={() => {
                set(!open);
              }}
            >
              <IoCloseSharp />
            </button>
          </div>
        </div>
        <div className="h-full">
          <DeepChat
            introMessage={{ text: "Send a Message to start the conversation." }}
            style={{
              borderRadius: "10px",
              width: `${fullsize ? "100vw" : null}`,
              height: `${fullsize ? "90vh" : null}`,
            }}
            textInput={{ placeholder: { text: "Ask Me About Prakriti" } }}
            request={{ url: "http://127.0.0.1:8000/chat", method: "POST" }}
          />
        </div>
        <div className="relative hidden">
          <div className="h-3/4">lorem</div>
          <div className="relative bottom-">
            <input
              type="text"
              name="message"
              id="msg"
              // onChange={(e) => setQueries(e.target.value)}
            />
            <button type="button">
              <IoSend />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

Chatbot.propTypes = {
  open: PropTypes.bool,
  set: PropTypes.func,
};

export default Chatbot;
