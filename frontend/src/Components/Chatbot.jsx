import PropTypes from "prop-types";
import { useCallback, useEffect, useRef, useState } from "react";
import { IoCloseSharp } from "react-icons/io5";
import "animate.css";
import { FiMaximize2, FiMinimize2 } from "react-icons/fi";
import { BsFillSendFill } from "react-icons/bs";
import Messages from "./Messages";
import chatanim from "../Assets/chatanim.gif";
import ChatAPI from "../Config";

const Chatbot = ({ open, set }) => {
  const [queries, setQueries] = useState([]);
  const [fullsize, setFullSize] = useState(false);
  const inputRef = useRef();
  const messageRef = useRef();
  const [websckt, setWebsckt] = useState();

  const ScrolltoBottom = () => {
    if (messageRef.current) {
      const container = messageRef.current;
      container.scrollTop = container.scrollHeight;
    }
  };

  useEffect(() => {
    // Scroll to the bottom whenever messages change
    ScrolltoBottom();
  }, [queries]);

  useEffect(() => {
    const ws = new WebSocket(`${ChatAPI}/chat`);
    ws.onopen = () => {
      ws.onmessage = (e) => {
        const message = JSON.parse(e.data);
        setQueries((old) => [...old, message]);
      };
      setWebsckt(ws);
    };
    inputRef.current.focus();
    return () => {
      ws.close();
    };
  }, []);

  const handleClick = useCallback(() => {
    if (inputRef.current.value === "") {
      return;
    }
    const sendingMessage = { name: "User", message: inputRef.current.value };
    setQueries((old) => [...old, sendingMessage]);
    websckt.send(JSON.stringify(sendingMessage));
    websckt.onmessage = (e) => {
      const message = JSON.parse(e.data);
      setQueries((old) => [...old, message]);
    };
    inputRef.current.value = "";
  }, [websckt]);

  return (
    <div className="relative h-full flex justify-center flex-col">
      <div
        className={`z-30 self-center rounded-lg border-4 border-sky-400  pb-5 bg-white animate__animated animate__fadeIn ${
          fullsize
            ? "w-full h-screen top-0 fixed"
            : "w-[90%] sm:w-[400px] fixed sm:top-[15%] top-3 sm:right-7 h-[95%] md:h-fit"
        }`}
      >
        <div className="bg-sky-400 font-playpen text-white px-3 py-2 flex flex-row justify-between text-lg font-serif items-center">
          <span className="flex flex-row gap-3 text-lg items-center">
            AyurBot
            <img src={chatanim} className="w-10" />
          </span>
          <div className="space-x-3">
            <button
              type="button"
              className="hover:bg-sky-400"
              onClick={() => {
                setFullSize(!fullsize);
              }}
            >
              {!fullsize ? (
                <FiMaximize2 size={20} />
              ) : (
                <FiMinimize2 size={20} />
              )}
            </button>
            <button
              className="hover:bg-sky-400"
              type="button"
              onClick={() => {
                set(!open);
              }}
            >
              <IoCloseSharp size={20} />
            </button>
          </div>
        </div>
        <div
          className={`relative ${
            fullsize ? "h-[88%]" : "h-96"
          } pt-4 pl-4 pb-4 mb-4 overflow-scroll`}
          ref={messageRef}
        >
          <div className="relative flex flex-col gap-2">
            <Messages queries={queries} />
          </div>
        </div>
        <div className="flex flex-row items-center justify-between gap-3 absolute w-full bottom-0 p-2">
          <input
            ref={inputRef}
            type="text"
            name="query"
            id="messageinput"
            placeholder="Type Your message here"
            className="px-4 py-2 border-gray-400 rounded-full outline-none border-2 w-full font-lora"
            onKeyDown={(e) => {
              if (e.key == "Enter") {
                handleClick();
              }
            }}
          />
          <button
            type="button"
            className="p-3 bg-gradient-to-r from-blue-600 from-20% to-sky-400 text-white rounded-lg px-6 transition-colors hover:bg-gradient-to-l hover:from-blue-600 hover:to-sky-400 hover:from-20% "
            id="sendbutton"
            onClick={handleClick}
          >
            <BsFillSendFill size={20} />
          </button>
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
