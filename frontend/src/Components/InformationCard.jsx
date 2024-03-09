import Proptypes from "prop-types";
import { useState } from "react";
import { motion } from "framer-motion";

function InformationCard({ icon, title, description, image, colorclass }) {
  const [hovered, setHovered] = useState(false);
  return (
    <div
      className="info-cards"
      onMouseOver={() => setHovered(true)}
      onMouseOut={() => setHovered(false)}
    >
      <span className="info-card-icon">{icon}</span>
      {!hovered ? (
        <div>
          <p className="info-card-title">{title}</p>
          <p className="info-card-description">{description}</p>
        </div>
      ) : (
        <motion.div
          className={`h-full rounded-md border-2 ${colorclass}`}
          initial={{ height: 0 }}
          animate={{ height: "100%" }}
          transition={{ duration: 1.6 }}
        >
          <motion.div
            className="flex justify-center items-center"
            initial={{ rotateX: 90 }}
            transition={{ duration: 1.6, delay: 0.7 }}
            whileInView={{ rotateX: 0 }}
            whileHover={{
              rotateY: [0, 90],
              transition: {
                repeat: Infinity,
                duration: 1,
                repeatType: "reverse",
              },
            }}
          >
            <img src={image} alt="Vata Image" className="w-1/2 my-10" />
          </motion.div>
        </motion.div>
      )}
    </div>
  );
}

InformationCard.propTypes = {
  icon: Proptypes.element,
  title: Proptypes.string,
  description: Proptypes.string,
  image: Proptypes.string,
  colorclass: Proptypes.string,
};

export default InformationCard;
