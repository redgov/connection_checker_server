from src.db_setting import ModelBase, Engine

# 以下はalembic利用時ModelBaseをインポートした際、
# 一緒にmodel情報まで読み込ませるため
from src.models import (
    GroupModel,
    MachineModel,
    MailAddressModel,
    MailAddressToMachineModel,
)
