from tiktoken import encoding_for_model
from langgraph.graph.message import BaseMessage

def count_tokens(messages: list[BaseMessage]) -> int:
    """
    Count tokens in a list of messages.
    Using tiktoken for token counting - adjust encoding based on your model.
    """
    encoding = encoding_for_model("gpt-3.5-turbo")  # Use as approximation for Llama
    num_tokens = 0
    
    for message in messages:
        # Count tokens in the message content
        num_tokens += len(encoding.encode(message.content))
        # Add tokens for message type/role (approximate)
        num_tokens += 4  # Approximate overhead per message
    
    return num_tokens

def trim_messages(messages: list[BaseMessage], max_tokens: int = 4000) -> list[BaseMessage]:
    """
    Trim messages to fit within token limit while preserving most recent context.
    """
    if not messages:
        return messages
    
    # Always keep the system message if it exists
    system_message = None
    chat_messages = messages.copy()
    
    if messages[0].type == "system":
        system_message = chat_messages.pop(0)
    
    # Count tokens in current messages
    current_tokens = count_tokens(chat_messages)
    
    # Remove oldest messages until we're under the limit
    while current_tokens > max_tokens and len(chat_messages) > 1:
        # Remove the oldest message (after system message)
        chat_messages.pop(0)
        current_tokens = count_tokens(chat_messages)
    
    # Add back system message if it existed
    if system_message:
        chat_messages.insert(0, system_message)

    for message in chat_messages:
        print(message)

    return chat_messages