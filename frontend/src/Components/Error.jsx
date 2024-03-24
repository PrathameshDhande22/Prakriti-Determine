import { motion } from "framer-motion";

const Error = () => {
  return (
    <motion.div
      className="text-center bg-red-500 text-white w-full py-3 px-3 rounded-b-md absolute bottom-0 font-bold"
      animate={{ backgroundColor: ["#ff0000", "#ff9500"] }}
      transition={{
        duration: 1.5,
        repeat: Infinity,
        repeatType: "reverse",
      }}
    >
      Error While Connecting to Server ...
    </motion.div>
  );
};
export default Error;
