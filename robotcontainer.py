#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib

import constants

from commands.autos import Autos
from commands.launchnote import LaunchNote
from commands.preparelaunch import PrepareLaunch

import commands2

from subsystems.drivetrain import DriveSubsystem
from subsystems.launcher import LauncherSubsystem
from subsystems.climber import ClimberSubsystem

from wpilib import SendableChooser

# from subsystems.pwm_drivesubsystem import DriveSubsystem
# from subsystems.pwm_launchersubsystem import LauncherSubsystem

def deadband(x):

    return x if abs(x) >= 0.2 else 0

class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        # The driver's controller
        self.driverController = wpilib.XboxController(
            constants.kDriverControllerPort
        )

        # The robot's subsystems
        self.drive = DriveSubsystem()
        self.launcher = LauncherSubsystem()
        self.climber = ClimberSubsystem()

        self.configureButtonBindings()

        self.drive.setDefaultCommand(
            # A split-stick arcade command, with forward/backward controlled by the left
            # hand, and turning controlled by the right.
            commands2.cmd.run(
                lambda: self.drive.arcadeDrive(
                    deadband(self.driverController.getLeftY()),
                    deadband(-self.driverController.getRightX()/2),
                    self.driverController.getBButton()
                ),
                self.drive,
            )
        )

       # self.chooser = SendableChooser()
        
        # self.chooser.setDefaultOption("None", None)
        # self.chooser.addOption("Leave", Autos.exampleAuto(self.drive, self.launcher))
        # self.chooser.addOption("Front Speaker", Autos.speaker_center(self.drive, self.launcher))
        # self.chooser.addOption("Blue Amp Side Speaker", Autos.amp_side_speaker(self.drive, self.launcher, 1))
        # self.chooser.addOption("Blue Feed Side Speaker", Autos.feed_side_speaker(self.drive, self.launcher, 1))
        # self.chooser.addOption("Red Amp Side Speaker", Autos.amp_side_speaker(self.drive, self.launcher, -1))
        # self.chooser.addOption("Red Feed Side Speaker", Autos.feed_side_speaker(self.drive, self.launcher, -1))

        #wpilib.SmartDashboard.putData("Auto Select", self.chooser)




    def configureButtonBindings(self):

        commands2.button.JoystickButton(self.driverController, wpilib.XboxController.Button.kRightBumper).whileTrue(PrepareLaunch(self.launcher)
            .withTimeout(constants.kLauncherDelay)
            .andThen(LaunchNote(self.launcher))
            .handleInterrupt(lambda: self.launcher.stop()))

        commands2.button.JoystickButton(self.driverController, wpilib.XboxController.Button.kLeftBumper).whileTrue(self.launcher.getIntakeCommand())
        commands2.button.JoystickButton(self.driverController, wpilib.XboxController.Button.kY).whileTrue(self.climber.climb_positive())
        commands2.button.JoystickButton(self.driverController, wpilib.XboxController.Button.kA).whileTrue(self.climber.climb_negative())
    def getAutonomousCommand(self) -> commands2.Command:
        pass
       # Autos.exampleAuto(self.drive)