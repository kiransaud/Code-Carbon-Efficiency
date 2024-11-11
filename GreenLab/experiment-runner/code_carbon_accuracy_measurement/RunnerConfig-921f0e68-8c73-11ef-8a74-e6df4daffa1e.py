

import os
import subprocess
from turtle import pd
from EventManager.Models.RunnerEvents import RunnerEvents
from EventManager.EventSubscriptionController import EventSubscriptionController
from ConfigValidator.Config.Models.RunTableModel import RunTableModel
from ConfigValidator.Config.Models.FactorModel import FactorModel
from ConfigValidator.Config.Models.RunnerContext import RunnerContext
from ConfigValidator.Config.Models.OperationType import OperationType
from ExtendedTyping.Typing import SupportsStr
from ProgressManager.Output.OutputProcedure import OutputProcedure as output
from codecarbon import  EmissionsTracker

from typing import Dict, List, Any, Optional
from pathlib import Path
from os.path import dirname, realpath

from Plugins.Profilers import CodecarbonWrapper
from Plugins.Profilers.CodecarbonWrapper import DataColumns as CCDataCols

@CodecarbonWrapper.emission_tracker(
    data_columns=[CCDataCols.CPU_ENERGY, CCDataCols.GPU_ENERGY,CCDataCols.RAM_ENERGY,CCDataCols.ENERGY_CONSUMED,CCDataCols.OS,CCDataCols.CPU_MODEL,
                  CCDataCols.GPU_MODEL,CCDataCols.CPU_COUNT,CCDataCols.GPU_COUNT,CCDataCols.RAM_TOTAL_SIZE,CCDataCols.TIMESTAMP,CCDataCols.DURATION],
    country_iso_code="NLD" # your country code
)


class RunnerConfig:
    ROOT_DIR = Path(dirname(realpath(__file__)))

    # ================================ USER SPECIFIC CONFIG ================================
    """The name of the experiment."""
    name = "code_carbon_accuracy_measurement"

    """The path in which Experiment Runner will create a folder with the name `self.name`, in order to store the
    results from this experiment. (Path does not need to exist - it will be created if necessary.)
    Output path defaults to the config file's path, inside the folder 'experiments'"""
    results_output_path:        Path            = ROOT_DIR / 'experiments'

    """Experiment operation type. Unless you manually want to initiate each run, use `OperationType.AUTO`."""
    operation_type:             OperationType   = OperationType.AUTO

    """The time Experiment Runner will wait after a run completes.
    This can be essential to accommodate for cooldown periods on some systems."""
    time_between_runs_in_ms:    int             = 1000

    # Dynamic configurations can be one-time satisfied here before the program takes the config as-is
    # e.g. Setting some variable based on some criteria
    def __init__(self):
        """Executes immediately after program start, on config load"""

        EventSubscriptionController.subscribe_to_multiple_events([
            (RunnerEvents.BEFORE_EXPERIMENT, self.before_experiment),
            (RunnerEvents.BEFORE_RUN       , self.before_run       ),
            (RunnerEvents.START_RUN        , self.start_run        ),
            (RunnerEvents.START_MEASUREMENT, self.start_measurement),
            (RunnerEvents.INTERACT         , self.interact         ),
            (RunnerEvents.STOP_MEASUREMENT , self.stop_measurement ),
            (RunnerEvents.STOP_RUN         , self.stop_run         ),
            (RunnerEvents.POPULATE_RUN_DATA, self.populate_run_data),
            (RunnerEvents.AFTER_EXPERIMENT , self.after_experiment )
        ])
        self.run_table_model = None  # Initialized later

        output.console_log("Custom config loaded")

    def create_run_table_model(self) -> RunTableModel:
        """Create and return the run_table model here. A run_table is a List (rows) of tuples (columns),
        representing each run performed"""
        scripts=[ f for f in os.listdir('./scripts')if f.endswith('.py')]
        python_script = FactorModel("script_name", scripts)
        repetition_number = FactorModel("repetition_number",list(range(1,16)))
        measure_power_sec=FactorModel('measure_power_secs',[5,15,30])
        tracking_mode=FactorModel('tracking_mode',["machine","process"])
        log_level=FactorModel('log_level',['debug','info','warning','error','critical'])

        
        self.run_table_model = RunTableModel(
            factors=[python_script,repetition_number,measure_power_sec,tracking_mode,log_level],
            # exclude_variations=[
            #     {factor1: ['example_treatment1']},                   # all runs having treatment "example_treatment1" will be excluded
            #     {factor1: ['example_treatment2'], factor2: [True]},  # all runs having the combination ("example_treatment2", True) will be excluded
            # ],
            # data_columns=['device_id','measurement_type','execution_time', 'cpu_energy','gpu_energy','ram_energy', 'total_energy','cpu_model','gpu_model','ram_size','os']
        )
        return self.run_table_model

    def before_experiment(self) -> None:
        """Perform any activity required before starting the experiment here
        Invoked only once during the lifetime of the program."""

        output.console_log("Config.before_experiment() called!")

    def before_run(self) -> None:

        """Perform any activity required before starting a run.
        No context is available here as the run is not yet active (BEFORE RUN)"""
        
        output.console_log("Config.before_run() called!")

    def start_run(self, context: RunnerContext) -> None:
        """Perform any activity required for starting the run here.
        For example, starting the target system to measure.
        Activities after starting the run should also be performed here."""
        # measure_power_secs = context.run_variation['measure_power_secs']
        # tracking_mode=context.run_variation['tracking_mode']
        # log_level=context.run_variation['log_level']
        # self.tracker = EmissionsTracker(output_dir='outputs', measure_power_secs=measure_power_secs, tracking_mode=tracking_mode, log_level=log_level)
        # self.tracker.start()
        script_name=context.run_variation['script_name']
        subprocess.run(['python3', os.path.join('scripts', script_name)], check=True)
        output.console_log("Config.start_run() called!")

    def start_measurement(self, context: RunnerContext) -> None:
        """Perform any activity required for starting measurements."""
        # script_name=context.run_variation['script_name']
        # subprocess.run(['python3', os.path.join('scripts', script_name)], check=True)

        output.console_log("Config.start_measurement() called!")

    def interact(self, context: RunnerContext) -> None:
        """Perform any interaction with the running target system here, or block here until the target finishes."""

        output.console_log("Config.interact() called!")

    def stop_measurement(self, context: RunnerContext) -> None:
        """Perform any activity here required for stopping measurements."""
    

        output.console_log("Config.stop_measurement called!")

    def stop_run(self, context: RunnerContext) -> None:
        """Perform any activity here required for stopping the run.
        Activities after stopping the run should also be performed here."""
        # self.tracker.stop()

        output.console_log("Config.stop_run() called!")

    def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, SupportsStr]]:
        """Parse and process any measurement data here.
        You can also store the raw measurement data under `context.run_dir`
        Returns a dictionary with keys `self.run_table_model.data_columns` and their values populated"""
    
        # cc_data = pd.read_csv(os.path.join('outputs'), "emissions.csv")

        output.console_log("Config.populate_run_data() called!")
        return None

    def after_experiment(self) -> None:
        """Perform any activity required after stopping the experiment here
        Invoked only once during the lifetime of the program."""

        output.console_log("Config.after_experiment() called!")

    # ================================ DO NOT ALTER BELOW THIS LINE ================================
    experiment_path:            Path             = None
