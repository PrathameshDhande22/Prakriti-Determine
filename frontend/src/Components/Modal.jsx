import PropTypes from "prop-types";
import { BsExclamationCircle } from "react-icons/bs";
import { IoIosCloseCircle } from "react-icons/io";

const Modal = ({ modalOpen, setModalOpen, title, assets }) => {
  return (
    <div
      className={`fixed top-0 bg-black/40 h-screen z-[200] w-screen animate__animated animate__fadeIn left-0 ${
        modalOpen ? "visible" : "hidden"
      }`}
    >
      <div className="flex justify-center w-full md:items-center top-5 md:top-0 relative h-full">
        <div className="bg-white relative  md:h-4/5 h-[90%] text-black w-4/5 lg:w-10/12 rounded-lg">
          <div className="flex flex-row md:text-xl text-white font-lora tracking-wide p-3 bg-cyan-500 items-center gap-5 justify-between rounded-t-lg">
            <span className="font-bold capitalize">{title}</span>
            <button type="button" onClick={setModalOpen}>
              <IoIosCloseCircle size={30} />
            </button>
          </div>
          <div className="relative overflow-y-scroll overflow-x-scroll h-[85%] px-4 mt-3">
            {Object.keys(assets).length !== 0 ? (
              <>
                <span className="flex flex-row gap-3 px-3 items-center justify-center">
                  <BsExclamationCircle size={18} />
                  <span className="text-xs">
                    The images utilized below are for illustrative purposes
                    only. They have been sourced from the internet, and some are
                    personal images used for demonstration purposes
                  </span>
                </span>
                <div className="flex flex-col justify-center gap-2 items-center pt-4">
                  {assets?.images.map((value, index) => {
                    return (
                      <img src={value} alt={`Image ${index}`} key={index} />
                    );
                  })}
                </div>
                {assets?.description && (
                  <div className="flex flex-col gap-3 items-center pt-5">
                    {assets?.description.map((value, index) => {
                      return (
                        <div
                          key={index}
                          className="font-lora md:text-lg text-base text-justify lg:w-1/2 w-full"
                        >
                          <span className="font-bold block font-playpen capitalize">
                            {value[0]} :{" "}
                          </span>
                          <span>{value[1]}</span>
                        </div>
                      );
                    })}
                  </div>
                )}
              </>
            ) : (
              <div className="flex flex-col gap-5 justify-center items-center h-[88%]">
                <div className="flex flex-col justify-center items-center">
                  <IoIosCloseCircle size={80} color="red" />
                  <span className="uppercase font-playpen text-xl font-semibold">
                    NO Description Added !
                  </span>
                </div>
                <div className="font-lora text-lg">
                  The question is kept simple and easy to understand by not
                  including any additional details.
                </div>
              </div>
            )}
            <div className="relative float-right mb-1">
              <button
                type="button"
                className="font-lora md:text-lg rounded-xl bg-red-500 md:px-8 px-3 py-2 text-white"
                onClick={setModalOpen}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default Modal;

Modal.propTypes = {
  modalOpen: PropTypes.bool,
  setModalOpen: PropTypes.func,
  title: PropTypes.string,
  assets: PropTypes.object,
};
