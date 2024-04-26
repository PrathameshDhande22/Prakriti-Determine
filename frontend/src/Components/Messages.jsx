import PropTypes from "prop-types";
import UserMessage from "./UserMessage";
import { BotMessage } from "./ChatMessage";
import { memo } from "react";

const Messages = ({ queries }) => {
  return (
    <>
      {queries.map((value, index) => {
        if (value.name == "User") {
          return <UserMessage key={index} message={value.message} />;
        }
        return <BotMessage key={index} message={value.message} />;
      })}
    </>
  );
};

const MemoizedMessages = memo(Messages);
export default MemoizedMessages;

Messages.propTypes = {
  queries: PropTypes.array,
};
