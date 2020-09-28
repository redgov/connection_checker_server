from src.db_setting import Session
from src.responses.machines import MachinesOut, MachineInfo
from src.models.machine import MachineModel


session = Session()


class MachinesService:

    def get(self):
        """マシン情報取得
        """
        machine_models = MachineModel.get()
        machines_out = MachinesOut(machines=[
            MachineInfo.from_orm(m)
            for m in machine_models
        ])
        return machines_out

    def create(self, group_id: int, name: str, ip_address: str):
        """新規マシン作成

        Parameters
        ----------
        group_id : int
            マシンが紐づくグループのID
        name : str
            マシン名
        ip_address : str
            マシンのIPアドレス
        """
        MachineModel.save(group_id, name, ip_address)
        session.commit()
