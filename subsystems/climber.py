import commands2
from phoenix6.configs import TalonFXConfiguration
from phoenix6.configs.config_groups import NeutralModeValue
from phoenix6.controls import DutyCycleOut
from phoenix6.hardware import TalonFX
import constants

class ClimberSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.setName("Climb")

        self.climbMotor = TalonFX(constants.climbMotor)
        climbing_config = TalonFXConfiguration()
        climbing_config.motor_output.with_neutral_mode(NeutralModeValue.BRAKE)

    def climb(self) -> None:
        self.climbMotor.set_control(DutyCycleOut(0.3, enable_foc=True))
        
        
