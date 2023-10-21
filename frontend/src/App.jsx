import "./App.css";
import About from "./Components/About";
import { ChatbotButton } from "./Components/ChatbotButton";
import Footer from "./Components/Footer";
import Hero from "./Components/Front";
import Info from "./Components/Info";
import Navbar from "./Components/Navbar";

function App() {
  return (
    <div className="App">
      <Navbar />
      <Hero />
      <ChatbotButton/>
      <Info/>
      <About/>
      <Footer/>
    </div>
  );
}

export default App;
