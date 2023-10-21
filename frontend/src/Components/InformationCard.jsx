import Proptypes from "prop-types";

function InformationCard({ icon, title, description }) {
  return (
    <div className="info-cards">
      <span className="info-card-icon">{icon}</span>
      <p className="info-card-title">{title}</p>
      <p className="info-card-description">{description}</p>
    </div>
  );
}

InformationCard.propTypes = {
  icon: Proptypes.element,
  title: Proptypes.string,
  description: Proptypes.string,
};

export default InformationCard;
