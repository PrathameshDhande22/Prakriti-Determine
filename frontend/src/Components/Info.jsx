import InformationCard from "./InformationCard";
import "../Styles/Info.css";
import { IoEarth, IoWaterSharp } from "react-icons/io5";
import { BsFire } from "react-icons/bs";
import vataImg from "../Assets/vata.png";
import pittaImg from "../Assets/pitta.png";
import kaphaImg from "../Assets/kapha.png";

function Info() {
  return (
    <div className="info-section" id="services">
      <div className="info-title-content">
        <h3 className="info-title">
          <span>What We Do</span>
        </h3>
        <p className="info-description">
          We combine ancient Ayurvedic wisdom with cutting-edge technology to
          provide personalized wellness guidance. Our chatbot assesses your
          Prakriti, or constitution, and offers tailored diet and lifestyle
          recommendations to help you achieve balance and harmony in your life.
        </p>
      </div>

      <div className="info-cards-content">
        <InformationCard
          title="Vata"
          description="Vata is associated with the elements of air and space. It is characterized by qualities of being dry, light, cold, rough, subtle, mobile, and clear. Vata is responsible for essential bodily functions such as breathing, circulation, and communication between cells. When in balance, Vata individuals are creative, energetic, and enthusiastic. However, an excess of Vata can lead to issues like anxiety, insomnia, and digestive problems."
          icon={<IoEarth className="info-fa-icon-earth" />}
          image={vataImg}
          colorclass={"bg-green-300 border-green-600"}
        />

        <InformationCard
          title="Pitta"
          description="Pitta embodies the elements of fire and water. It exhibits qualities of being hot, sharp, oily, light, and spreading. Pitta governs metabolic and transformative processes in the body, including digestion, absorption, and temperature regulation. Balanced Pitta types are intelligent, courageous, and focused. Excessive Pitta can manifest as irritability, inflammation, or digestive disorders."
          icon={<BsFire className="info-fa-icon-fire" />}
          image={pittaImg}
          colorclass={"bg-yellow-300 border-orange-600"}
        />

        <InformationCard
          title="Kapha"
          description="Kapha is primarily composed of earth and water elements, giving it qualities of heaviness, cold, oily, smooth, and static. Kapha oversees stability, growth, and lubrication within the body. Individuals with balanced Kapha are calm, strong, and compassionate. However, an excess of Kapha can lead to weight gain, lethargy, and respiratory problems."
          icon={<IoWaterSharp className="info-fa-icon" />}
          image={kaphaImg}
          colorclass={"bg-blue-200 border-blue-600"}
        />
      </div>
    </div>
  );
}

export default Info;
