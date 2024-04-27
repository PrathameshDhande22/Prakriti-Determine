import { memo } from "react";
import { FaShareFromSquare } from "react-icons/fa6";
import PropTypes from "prop-types";

const ShareButton = ({ dosha }) => {
  const handleOnClick = async () => {
    try {
      await window.navigator.share({
        text: `*My Prakriti is ${dosha}*\n\nWhat's yours? You can also discover your Prakriti on AyurInsights.\n\nCheck now! 👉 ${window.location.href}\n\nEver wondered about your Prakriti? I found out I'm ${dosha}! Head over to AyurInsights to reveal yours! 🔍`,
      });
    } catch (e) {
      alert(
        "WebShare is Not Supported in Your Browser.\nPlease Update your Browser."
      );
    }
  };
  return (
    <div className="space-y-1">
      <span>Share Your Prakriti with Others : </span>
      <button
        type="button"
        onClick={handleOnClick}
        className="flex flex-row gap-3 items-center py-1 px-5 rounded-lg border-2 border-gray-400 bg-gray-100 hover:bg-gray-300 hover:border-gray-600 transition-all active:bg-white"
      >
        <span className="text-base font-playpen">Share</span>
        <FaShareFromSquare size={20} color="blue" />
      </button>
    </div>
  );
};

const ShareButtonMemoized = memo(ShareButton);
export default ShareButtonMemoized;

ShareButton.propTypes = {
  dosha: PropTypes.string,
};
