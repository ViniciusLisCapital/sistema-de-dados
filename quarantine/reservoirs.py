
#_importar pacotes
import pandas as pd


#_arquivos
ear_2000 = pd.read_csv("https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/ear_reservatorio_di/EAR_DIARIO_RESERVATORIOS_2000.csv", sep = ';')



#_tratamento
ear_2000.drop(columns = ['cod_resplanejamento', 'tip_reservatorio', 'nom_ree','id_subsistema', 'id_subsistema_jusante', 'ear_reservatorio_subsistema_jusante_mwmes', 'earmax_reservatorio_subsistema_jusante_mwmes'], inplace  = True)

