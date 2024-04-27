import { FaFilePdf } from "react-icons/fa6";
import PropTypes from "prop-types";
import { memo, useEffect, useState } from "react";

const DownloadButton = ({ blob }) => {
  const [pdfBlob, setBlob] = useState(null);

  useEffect(() => {
    const pdfBytes = new Blob([blob], { type: "application/pdf" });
    setBlob(pdfBytes);
  }, [blob]);

  const handleClick = () => {
    if (pdfBlob) {
      const url = URL.createObjectURL(pdfBlob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "Diet Plan.pdf");
      link.click();
    }
  };

  return (
    <div className="flex flex-row flex-wrap items-center gap-1">
      <span>Download Your Recommendation in PDF Format : </span>
      <button
        type="button"
        onClick={handleClick}
        className="flex flex-row items-center gap-3 py-1 px-5 border-2 border-gray-400 bg-gray-100 rounded-lg hover:bg-gray-300 hover:border-gray-600 transition-all"
      >
        <FaFilePdf size={20} color="red" />
        <span className="font-lora font-semibold">Download</span>
      </button>
    </div>
  );
};
export const MemoizedDownload = memo(DownloadButton);

DownloadButton.propTypes = {
  blob: PropTypes.any,
};
