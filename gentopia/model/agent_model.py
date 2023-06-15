from enum import Enum

from pydantic import BaseModel


class AgentType(Enum):
    """
    Enumerated type for agent types.
    """
    REACT = "react"
    REWOO = "rewoo"
    DIRECT = "direct"

    @staticmethod
    def get_agent_class(_type: 'AgentType'):
        """
        Get agent class from agent type.
        :param _type: agent type
        :return: agent class
        """
        if _type == AgentType.REACT:
            from gentopia.agent.react import ReactAgent
            return ReactAgent
        elif _type == AgentType.REWOO:
            from gentopia.agent.rewoo import RewooAgent
            return RewooAgent
        elif _type == AgentType.DIRECT:
            from gentopia.agent.vanilla import VanillaAgent
            return VanillaAgent
        else:
            raise ValueError(f"Unknown agent type: {_type}")


class AgentOutput(BaseModel):
    """
    Pydantic model for agent output.
    """
    output: str
    cost: float
    token_usage: int