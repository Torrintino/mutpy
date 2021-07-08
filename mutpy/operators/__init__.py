from .arithmetic import *
from .base import *
from .decorator import *
from .exception import *
from .inheritance import *
from .logical import *
from .loop import *
from .misc import *

SuperCallingInsert = utils.get_by_python_version([
    SuperCallingInsertPython27,
    SuperCallingInsertPython35,
])

standard_operators = {
    ArithmeticOperatorDeletion,
    ArithmeticOperatorReplacement,
    AssignmentOperatorReplacement,
    BreakContinueReplacement,
    ConditionalOperatorDeletion,
    ConditionalOperatorInsertion,
    ConstantReplacement,
    DecoratorDeletion,
    ElifBranchDeletion,
    ExceptionHandlerDeletion,
    ExceptionSwallowing,
    GenericLoopSkip,
    HidingVariableDeletion,
    LogicalConnectorReplacement,
    LogicalOperatorDeletion,
    LogicalOperatorReplacement,
    OpenEncodingReplacement,
    OpenModeReplacement,
    OverriddenMethodCallingPositionChange,
    OverridingMethodDeletion,
    RangeStepIncrement,
    RelationalOperatorReplacement,
    SliceIndexRemove,
    SuperCallingDeletion,
    SuperCallingInsert,
}

experimental_operators = {
    ClassmethodDecoratorInsertion,
    OneIterationLoop,
    ReverseIterationLoop,
    SelfVariableDeletion,
    StatementDeletion,
    StaticmethodDecoratorInsertion,
    ZeroIterationLoop,
}
