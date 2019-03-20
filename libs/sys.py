# !/usr/bin/env python
# encoding:utf-8
import datetime
import psutil
import time
import subprocess
import paramiko
import pymysql
from libs.util import TextOp, Debug


def get_now_time():
	localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	return localtime


class Sys(object):
	def __init__(self):
		pass
	
	@classmethod
	def shell_exec_single(cls, cmdstring, timeout=8):
		"""
		:param cmdstring: str, shell command
		:param timeout: int
		:return: str, execute result
		"""
		if timeout:
			end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
		sub = subprocess.Popen(cmdstring, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
		                       shell=True)
		while True:
			if sub.poll() is not None:
				break
			time.sleep(0.1)
			if timeout:
				if end_time <= datetime.datetime.now():
					sub.kill()
					return "TIME_OUT"
		return str(sub.stdout.read())
	
	@classmethod
	def get_time(cls):
		return get_now_time()
	
	@classmethod
	def get_mem_info(cls):
		"""
		:return: dict {total memsize, available memsize, free memsize}, MB
		"""
		memory_convent = 1024 * 1024
		mem = psutil.virtual_memory()
		
		dmi_str = Sys.shell_exec_single("dmidecode -t memory")
		t_list_mem_socket = TextOp.find_str(dmi_str, "P[1-9]-DIMM[A-Z]+[1-9]+$", False)
		max_mem_size = TextOp.find_str_column(dmi_str, "Maximum Capacity.+", 1, ":")
		t_list_mem_model = TextOp.find_str(dmi_str, "Part Number.{2}[^D].+", False)
		mem_dict = {}
		try:
			mem_dict = {
				"mem_socet_num": len(t_list_mem_socket),
				"max_mem_size": max_mem_size[0],
				"mem_model": t_list_mem_model[0],
				"total": mem.total / memory_convent,
				"available": mem.available / memory_convent,
				"free": mem.free / memory_convent
			}
		except Exception as ex:
			print(Debug.get_except(ex))
		if len(mem_dict) > 0:
			return mem_dict
		else:
			return None
	
	@classmethod
	def get_cpu_info(cls):
		"""
		:return: dict {socket_num, cpu_num, cpu_model, cpu_core, cpu_stepping}
		"""
		ret_dict = {}
		dmi_str = Sys.shell_exec_single("dmidecode -t processor")
		t_list_socket = TextOp.find_str(dmi_str, ".+Socket Designation.+", False)
		t_list_cpu_model = TextOp.find_str_column(dmi_str, ".+Version.+", 1, ":", False)
		t_list_cpu_core = TextOp.find_str_column(dmi_str, ".+Core Count:.+", 1, ":", False)
		t_list_cpu_stepping = TextOp.find_str_column(dmi_str, "Stepping [0-9]+", 1, " ", False)
		if t_list_socket is None:
			return {}
		try:
			ret_dict = {
				"socket_num": len(t_list_socket),
				"cpu_num": len(t_list_cpu_model),
				"cpu_model": str(t_list_cpu_model[0]),
				"cpu_core": int(str(t_list_cpu_core[0])),
				"cpu_stepping": str(t_list_cpu_stepping[0])
			}
		except Exception as ex:
			print(Debug.get_except(ex))
		if len(ret_dict) > 0:
			return ret_dict
		else:
			return None
	
	@classmethod
	def get_hba_info(cls):
		ret_dict = {}
		hba_list_str = Sys.shell_exec_single("sas3ircu list")
		hba_index_list = TextOp.find_str_column(hba_list_str, "[0-9]+ +(SAS|LSI)[0-9]{4}", 0, " ")[0]
		hba_chipset_list = TextOp.find_str_column(hba_list_str, "[0-9]+ +(SAS|LSI)[0-9]{4}", 1, " ")[0]
		if len(hba_index_list) == 0:
			return None
		i = 0
		while i < len(hba_index_list):
			i_str = hba_index_list[i]
			ret_dict[i_str]["chipset"] = hba_chipset_list[i]
			hba_status_str = Sys.shell_exec_single("sas3ircu 0 display")
			ret_dict[i_str]["fw"] = TextOp.find_str_column(hba_status_str, "Firmware version.+([0-9]|\.)+", 1, ":")[0]
			ret_dict[i_str]["bios"] = TextOp.find_str_column(hba_status_str, "BIOS version.+([0-9]|\.)+", 1, ":")[0]
			# dev_type_list = TextOp.find_str(hba_status_str, "Device is a.+")
			i += 1
	
	@classmethod
	def get_hwraid_info(cls):
		def _split(string):
			if isinstance(string, str):
				return string.split(":")[1]
		
		ret_dict = {}
		raid_list_str = Sys.shell_exec_single("storcli show")
		raid_index_list = \
		TextOp.find_str_column(raid_list_str, "[0-9]+ (LSI[0-9]{4}|([a-z]|[A-Z])+[0-9]{4}-[0-9]+(i|e))", 0, " ")[0]
		raid_chipset_list = \
		TextOp.find_str_column(raid_list_str, "[0-9]+ (LSI[0-9]{4}|([a-z]|[A-Z])+[0-9]{4}-[0-9]+(i|e))", 1, " ")[0]
		if len(raid_list_str) == 0:
			return None
		i = 0
		while i < len(raid_index_list):
			i_str = raid_index_list[i]
			ret_dict[i_str]["chipset"] = raid_chipset_list[i]
			raid_status_str = Sys.shell_exec_single("storcli /c{0} show".format(i_str))
			ret_dict[i_str]["fw"] = TextOp.find_str_column(raid_status_str, "FW Version.+", 1, "=")[0]
			ret_dict[i_str]["bios"] = TextOp.find_str_column(raid_status_str, "BIOS Version.+", 1, "=")[0]
			ret_dict[i_str]["driver"] = TextOp.find_str_column(raid_status_str, "Driver Version.+", 1, "=")[0]
			ret_dict[i_str]["sn"] = TextOp.find_str_column(raid_status_str, "Serial Number.+", 1, "=")[0]
			ret_dict[i_str]["sasaddr"] = TextOp.find_str_column(raid_status_str, "SAS Address.+", 1, "=")[0]
			disk_eid_list = TextOp.find_str_column(raid_status_str, "^[0-9]+:[0-9]+.+", 0, ":")
			disk_slt_list = list(map(_split, TextOp.find_str_column(raid_status_str, "^[0-9]+:[0-9]+.+", 0, " ")))
			disk_did_list = TextOp.find_str_column(raid_status_str, "^[0-9]+:[0-9]+.+", 1, " ")
			disk_state_list = TextOp.find_str_column(raid_status_str, "^[0-9]+:[0-9]+.+", 2, " ")
			disk_model_list = TextOp.find_str_column(raid_status_str, "", 11, " ")
			ret_dict[i_str]["disk"] = []
			for index, item in enumerate(disk_eid_list):
				disk_dict = {
					"slot": disk_slt_list[index],
					"eid": disk_eid_list[index],
					"state": disk_state_list[index],
					"did": disk_did_list[index],
					"model": disk_model_list[index]
				}
				ret_dict[i_str]["disk"].append(disk_dict)
			i += 1
	
	@classmethod
	def get_through_disk(cls):
		lsscsi_str = Sys.shell_exec_single("lsscsi")
	
	@classmethod
	def get_gpu_info(cls):
		dmi_str = Sys.shell_exec_single("dmidecode -t slot")
		dmi_slot_info = TextOp.find_str(dmi_str, "CPU.+SLOT.+|Current Usage.+|Bus Address.+", False)
		if len(dmi_slot_info) == 0:
			return None
		i = 0
		slot_dict = {}
		while i < len(dmi_slot_info):
			slot_dict["cpu"] = TextOp.find_str(dmi_slot_info[i], "CPU[0-9]+", False)
			slot_dict["slot"] = TextOp.find_str(dmi_slot_info[i], "SLOT[0-9]+", False)
			slot_dict["usage"] = TextOp.find_str(dmi_slot_info[i + 1], "In Use|Available", False)
			slot_dict["address"] = TextOp.find_str(dmi_slot_info[i + 2], "[0-9]+:[0-9]+:[0-9]+\.[0-9]+", False)
			i += 3
		gpu_id_str = Sys.shell_exec_single("nvidia-smi -a")
		return slot_dict
	
	@classmethod
	def collect_logs(cls):
		Sys.shell_exec_single("collector.sh")
	
	@classmethod
	def scp(cls, src, dist_ip, dist, username="root", passwd="000000"):
		try:
			transport = paramiko.Transport((dist_ip, 22))
			transport.connect(username=username, password=passwd)
			sftp = paramiko.SFTPClient.from_transport(transport)
			sftp.put(src, dist)
			transport.close()
		except Exception as  ex:
			print(Debug.get_except(ex))
	
	@classmethod
	def post_mysql_upload(cls, host, user, passwd, db, table, src_file, dist_file, port=3306):
		split_list = TextOp.split_str(src_file, "_")
		conn = pymysql.connect(host, port, user, passwd, db, charset='utf-8')
		cursor = conn.cursor()
		try:
			cursor.execute(
				"insert into {0}(file_name,file_path) values ('{1}','{2}')".format(table, split_list[0], dist_file))
			conn.commit()
		except Exception as ex:
			conn.rollback()
			print(Debug.get_except(ex))
		finally:
			cursor.close()
			conn.close()
