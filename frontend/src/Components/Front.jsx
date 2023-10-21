import BodyImg from "../Assets/mainimg1.jpg";
import { FaRobot } from "react-icons/fa";
import "../Styles/Front.css";

function Hero() {
  return (
    <div className="section-container">
      <div className="hero-section">
        <div className="text-section">
          <p className="text-headline">❤️ Health comes first</p>
          <h2 className="text-title">
            AyurBot: Personalized Ayurvedic Wellness Chatbot
          </h2>
          <p className="text-descritpion">
            Discover Your Ayurvedic Balance: Experience our AI-driven chatbot
            that determines your Prakriti and offers personalized dietary
            guidance for holistic well-being.
          </p>
          {/* TODO : Use these button to call the chat bot ui */}
          <button
            className="text-appointment-btn"
            type="button"
            // onClick={handleBookAppointmentClick}
          >
            <FaRobot size={20} />
            <span>Open Chat Bot</span>
          </button>
        </div>

        <div className="hero-image-section">
          <img className="hero-image1" src={BodyImg} alt="Doctor" />
        </div>
      </div>
    </div>
  );
}

export default Hero;
