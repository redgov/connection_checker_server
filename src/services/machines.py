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

    def edit(self,
             machine_id: int,
             group_id: int,
             name: str,
             address: str,
             is_active: bool) -> None:
        """マシン編集

        Parameters
        ----------
        machine_id : int
            編集対象のマシン
        group_id : int
            編集後のグループID
        name : str
            編集後のマシン名
        address : str
            編集後のipアドレス
        is_active : bool
            有効か否か
        """
        MachineModel.update(machine_id,
                            group_id,
                            name,
                            address,
                            is_active)
        session.commit()

    def delete(self, id: int) -> None:
        """指定されたマシン削除

        Parameters
        ----------
        id : int
            削除対象マシンID
        """
        MachineModel.delete(id)
        session.commit()
