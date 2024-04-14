import PropTypes from "prop-types";
import { RiRobot2Line } from "react-icons/ri";
import parse from "html-react-parser";
import { useContext, useState } from "react";
import { ChatSendMessage } from "./Chatbot";
import Modal from "./Modal";
import { BsExclamationCircle } from "react-icons/bs";
import { Tooltip } from "react-tooltip";

export const ChatMessage = ({ message }) => {
  const [selected, setSelected] = useState(false);
  const { handleClick } = useContext(ChatSendMessage);
  const [modalOpen, setModalOpen] = useState(false);

  const handleShowModal = () => {
    setModalOpen(true);
    if (typeof window != "undefined" && window.document) {
      document.body.style.overflow = "hidden";
    }
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    document.body.style.overflow = "unset";
  };

  if (typeof message === "string") {
    return (
      <>
        <div className="flex flex-row items-center gap-2 h-full">
          <RiRobot2Line size={18} className="text-blue-800" />
          <span className="bg-gray-200 p-2 w-[70%] animate__animated animate__faster animate__fadeIn  rounded-lg font-lora">
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
            <div className="w-[70%] animate__animated animate__faster animate__fadeIn">
              <div className="bg-gray-200 p-2 w-full  rounded-lg font-lora">
                {message["question"]}
              </div>
              <div className="w-full pt-1 flex gap-1">
                {Object.keys(message?.options).map((objkey, index) => {
                  return (
                    <div
                      key={index}
                      className={`w-full gap-1 flex flex-row justify-between items-center ${
                        selected && "hidden"
                      }`}
                    >
                      <input
                        type="radio"
                        name="confirmation"
                        id="confirmbtn"
                        className="hidden"
                        value={String(message?.options[objkey])}
                      />
                      <label
                        htmlFor="confirmbtn"
                        onClick={(e) => {
                          setSelected(true);
                          handleClick(e.target.dataset?.value);
                        }}
                        className="font-lora text-center hover:bg-blue-600 select-none hover:text-white  transition-colors capitalize border-2 border-gray-400 rounded-md w-full py-1 shadow-lg"
                        data-value={String(message?.options[objkey])}
                      >
                        {String(message?.options[objkey])}
                      </label>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </>
      );
    } else
      return (
        <>
          {message?.assets && (
            <Modal
              setModalOpen={handleCloseModal}
              modalOpen={modalOpen}
              assets={message?.assets}
              title={message["question"]}
            />
          )}
          <div className="flex flex-row items-center gap-2 h-full">
            <RiRobot2Line size={18} className="text-blue-800" />
            <div className="w-[70%] animate__animated animate__faster animate__fadeIn">
              <div className="bg-gray-200 flex flex-row justify-between items-center p-2 w-full rounded-lg font-lora ">
                <span>{parse(message["question"])}</span>
                {message?.assets && !selected && (
                  <button
                    type="button"
                    onClick={handleShowModal}
                    className="hover:bg-gray-300 p-1 rounded-lg active:bg-white"
                    data-tooltip-id="description-tooltip"
                    data-tooltip-content="Detailed Explanation of Question"
                  >
                    <BsExclamationCircle size={20} color="red" />
                  </button>
                )}
                <Tooltip id="description-tooltip" place="top" variant="dark"/>
              </div>
              <div
                className={`w-full pt-2 flex flex-col flex-wrap gap-2 items-center ${
                  selected && "hidden"
                }`}
              >
                {Object.keys(message?.options).map((objkey, index) => {
                  return (
                    <button
                      type="button"
                      key={index}
                      htmlFor="confirmbtn"
                      onClick={(e) => {
                        len == 3
                          ? handleClick(String(index), e.target.dataset?.value)
                          : handleClick(e.target.dataset?.value);
                        setSelected(true);
                      }}
                      className="font-lora text-center hover:bg-blue-600 select-none hover:text-white  transition-colors capitalize border-2 py-1 border-gray-400 rounded-md w-full shadow-lg"
                      data-value={String(message?.options[objkey])}
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
