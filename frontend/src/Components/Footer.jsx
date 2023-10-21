import "../Styles/Footer.css";
import Logo from "../Assets/Logo.png";

function Footer() {
  return (
    <div className="footer-section">
      <div className="footer-container">
        <div className="ft-info">
          <div className="ft-info-p1">
            <p className="ft-title">
              <a href="#">
                <img src={Logo} width={200} alt="Website's Logo" />
              </a>
            </p>
            <p className="ft-description">
              Your holistic journey to Ayurvedic well-being. Harness the wisdom
              of Ayurveda with our chatbot, designed to personalize your path to
              health. Discover your Prakriti, balance your doshas, and embrace a
              harmonious life.
            </p>
          </div>
        </div>

        <div className="ft-copyright">
          <p>© 2023 Ayurlnsights. All rights reserved.</p>
        </div>
        <div className="ft-developlist">
          Developed by Prathamesh Dhande, Chaitanya Mestry, Lonith Shetty &
          Goutam Thakur
        </div>
      </div>
    </div>
  );
}

export default Footer;
