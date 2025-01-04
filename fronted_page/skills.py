import streamlit as st

st.set_page_config(page_title='TYUT - 系统技术指南',  layout='wide', page_icon=':wrench:')
# Title the app
st.title('系统技术指南')
st.divider() 
st.markdown("""
 * 1 传感器: PulseSensor传感器 :star: https://pulsesensor.com/
 * 2 工作原理: 光电容积法原理 :star: https://blog.csdn.net/qq_44016222/article/details/141952478
 * 3 Arduino uno R3开发板(ArduinoIDE)
 * 4 前端: streamlit
 * 5 后端: FastAPI
 * 6 数据库: MySQL
""")

st.markdown("""
## 1.1 PulseSensor传感器简介
> PulseSensor传感器是一种基于光学原理的心率传感器，可以通过测量心脏跳动时的血液流动情况来检测心率。\n它由一个LED和一个光敏元件组成，LED发出的光线透过皮肤照射到血液中，光敏元件接收反射回来的光线，然后将光信号转换为电信号，从而测量出心率。
""")
col1, col2= st.columns(2)
#传感器图片
col1.image(r"D:\Users\Administrator\Desktop\sensor\fronted_page\pic_static\sensor1.png", 
                caption="PulseSensor传感器外型",width=600)
col2.image(r"D:\Users\Administrator\Desktop\sensor\fronted_page\pic_static\sensor2.png",caption="PulseSensor套件",width=600)
#小标题
st.markdown("""
## 1.2 烧录代码
* 代码1 :blue[main.c]文件 :computer:
""")

code1 = '''
#include "stm32f10x.h"
#include "led.h"
#include "usart.h"
#include "delay.h"
#include "oled.h"
#include "adcx.h"
#include "timer.h"

 
extern _Bool Timer_Flag ;			//时间到 标准位
extern _Bool update_flag;			//更新标志变量
 
//要写入到STM32 FLASH的字符串数组
u8 TEXT_Buffer[]={"0000000"};
#define SIZE sizeof(TEXT_Buffer)	 	//数组长度
//#define FLASH_SAVE_ADDR  0X08020000 	//设置FLASH 保存地址(必须为偶数，且其值要大于本代码所占用FLASH的大小+0X08000000)
#define FLASH_SAVE_ADDR  0X0800f400 	//设置FLASH 保存地址(必须为偶数，且其值要大于本代码所占用FLASH的大小+0X08000000)
 
 
int main(void)
{ 
	unsigned char p[16]=" ";
	u8 datatemp[SIZE];	
	_Bool Heart_OK = 0;				//读取到正确心率标志位
	unsigned char Heart = 0;		//心率值
	
  SystemInit();//配置系统时钟为72M	
	delay_init(72);
	LED_Init();
	LED_On();
 
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_3);//设置中断优先级分组为组3：2位抢占优先级，2位响应优先级
	
	USART1_Config();//串口初始化
	
	OLED_Init();
	printf("Start \n");
	delay_ms(1000);
	//显示“血氧:”
	OLED_ShowChinese(0,0,0,16,1);
	OLED_ShowChinese(16,0,1,16,1);
	OLED_ShowChar(32,0,':',16,1);
	
	ADCx_Init();
	TIM3_Int_Init(1999,71);			//定时2ms中断
	TIM2_Int_Init(199,7199);		//10Khz的计数频率，计数到500为20ms 
	
 
//  while (1)
//  {
//		LED_Toggle();
 
//		printf("光照强度: %d\r\n",light);
//		
//		OLED_ShowNum(80,0,light,3,16,1);
 
//		delay_ms(500);
//  }
 
 	while(1)
	{	
		if(Timer_Flag==1)					//500ms到 读取数据
		{
			Timer_Flag = 0;					//清除标志
			TIM_ITConfig(TIM2,TIM_IT_Update,DISABLE ); 						//使能指定的TIM3中断,允许更新中断
			TIM_ITConfig(TIM3,TIM_IT_Update,DISABLE ); 						//使能指定的TIM3中断,允许更新中断		
			delay_ms(500);
			TIM_ITConfig(TIM2,TIM_IT_Update,ENABLE ); 						//使能指定的TIM3中断,允许更新中断
			TIM_ITConfig(TIM3,TIM_IT_Update,ENABLE ); 						//使能指定的TIM3中断,允许更新中断
 
			TIM_Cmd(TIM2, ENABLE);  		//使能TIMx	
			if (QS == true)					//读取到了心率信号
			{			
				QS = false; 				//清除标志 等待下一次读取
				if(BPM>HEART_MIN_ERROR&&BPM<HEART_MAX_ERROR)		//读取到的值再正常心率区间 40-160内
				{
					Heart_OK = 1;			//标志位置一
					Heart = BPM;			//心率传递给Heart
				}
				else
				{
					Heart_OK = 0;			//标志位清零
					Heart = 0;				//设置为0
				}	
			}
		}
	
		delay_ms(20);	
 
		if(Heart_OK==1)								//读取到正确心率
		{
			OLED_ShowNum(40,0,Heart,3,16,1);
		}
		else
		{
			OLED_ShowString(32,0,":---r/min",16,1);
		}
 
	}	
}
 
'''
st.code(code1, language=None)

st.markdown("""
* 代码2 :blue[adc.c]文件 :computer:
""")
code2 = '''
#include "adcx.h"
#include "delay.h"
															   
void  ADCx_Init(void)
{ 	
	ADC_InitTypeDef   ADC_InitStructure;
	GPIO_InitTypeDef  GPIO_InitStructure;
	
	RCC_APB2PeriphClockCmd(PulseSensor_GPIO_CLK|ADC_CLK,ENABLE);
	RCC_ADCCLKConfig(RCC_PCLK2_Div6);
	
	//PA0
	GPIO_InitStructure.GPIO_Pin=PulseSensor_GPIO_PIN;
	GPIO_InitStructure.GPIO_Mode=GPIO_Mode_AIN;
	GPIO_Init(PulseSensor_GPIO_PORT,& GPIO_InitStructure);
	
	ADC_DeInit(ADCx);
	
	ADC_InitStructure.ADC_Mode = ADC_Mode_Independent;	//ADC工作模式:ADCx和ADC2工作在独立模式
	ADC_InitStructure.ADC_ScanConvMode = DISABLE;	      //模数转换工作在单通道模式
	ADC_InitStructure.ADC_ContinuousConvMode = DISABLE;	//模数转换工作在单次转换模式
//ADC_InitStructure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_None;	  //转换由软件而不是外部触发启动
	ADC_InitStructure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_T3_TRGO;//选择TIM3作为外部触发源
	ADC_InitStructure.ADC_DataAlign= ADC_DataAlign_Right;                	//ADC数据右对齐
	ADC_InitStructure.ADC_NbrOfChannel = 1;	                              //顺序进行规则转换的ADC通道的数目
	ADC_Init(ADCx, &ADC_InitStructure);	
	
	ADC_ExternalTrigConvCmd(ADCx,ENABLE);//采用外部触发
	ADC_RegularChannelConfig(ADCx, ADC_Channel_0, 1, ADC_SampleTime_239Cycles5);//adc转换时间21us
	ADC_Cmd(ADCx, ENABLE);
	
	ADC_ResetCalibration(ADCx);									//复位校准
	while(ADC_GetResetCalibrationStatus(ADCx));	//等待校准结束，校准结束状态为RESET
	ADC_StartCalibration(ADCx);									//AD校准
	while(ADC_GetCalibrationStatus(ADCx));			//等待校准结束	
 
}				  
//获得ADC值
//ch:通道值 0~3
u16 Get_Adc(u8 ch)   
{
  	//设置指定ADC的规则组通道，一个序列，采样时间
	ADC_RegularChannelConfig(ADCx, ch, 1, ADC_SampleTime_239Cycles5 );	//ADCx,ADC通道,采样时间为239.5周期	  			    
  
	ADC_SoftwareStartConvCmd(ADCx, ENABLE);		//使能指定的ADCx的软件转换启动功能	
	 
	while(!ADC_GetFlagStatus(ADCx, ADC_FLAG_EOC ));//等待转换结束
 
	return ADC_GetConversionValue(ADCx);	//返回最近一次ADCx规则组的转换结果
}
 
u16 Get_Adc_Average(u8 ch,u8 times)
{
	u32 temp_val=0;
	u8 t;
	for(t=0;t<times;t++)
	{
		temp_val+=Get_Adc(ch);
		delay_ms(5);
	}
	return temp_val/times;
} 	 
'''
st.code(code2, language=None)