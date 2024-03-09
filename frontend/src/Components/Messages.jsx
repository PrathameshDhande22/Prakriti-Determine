import PropTypes from "prop-types";
import UserMessage from "./UserMessage";
import { ChatMessage } from "./ChatMessage";

const Messages = ({ queries }) => {
  return (
    <>
      {queries.map((value, index) => {
        if (value.name == "User") {
          return <UserMessage key={index} message={value.message} />;
        }
        return <ChatMessage key={index} message={value.message} />;
      })}
    </>
  );
};
export default Messages;

Messages.propTypes = {
  queries: PropTypes.array,
};
