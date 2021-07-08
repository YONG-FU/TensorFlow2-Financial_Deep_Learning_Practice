from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import openpyxl

drug_trials_wb = openpyxl.load_workbook("drug_data/Generated - China Drug Trials.xlsx")
print(drug_trials_wb.sheetnames)
drug_trials_sheet = drug_trials_wb["Sheet1"]

year_string = str(2021)
# case_number_length_2021 = 1309
# case_number_length_2020 = 2712
# case_number_length_2019 = 2738
# case_number_length_2018 = 2561

for case_number in range(1, 2000):
    case_string = str(case_number).zfill(4)
    keyword = "CTR" + year_string + case_string
    print(keyword)

    row_index = case_number + 2

    # Load web pages into Python through requests urls
    browser = webdriver.Firefox()
    print("正在打开浏览网页...")

    url = "http://www.chinadrugtrials.org.cn/clinicaltrials.searchlistdetail.dhtml?keywords=" + keyword
    browser.get(url)
    print("正在等待页面加载...")

    try:
        wait = WebDriverWait(browser, 15)
        wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "searchDetailTable")))
        print("正在获取网页数据...")
    except Exception:
        browser.close()
        drug_trials_wb.save("drug_data/Generated - China Drug Trials.xlsx")
        continue

    soup = BeautifulSoup(browser.page_source, "lxml")
    browser.close()
    # print(soup.prettify())

    # Access elements and attributes inside HTML pages
    div_classes_filter = {"class": "sDPTit2"}
    divs = soup.find_all("div", div_classes_filter)
    print(len(divs))

    table_classes_filter = {"class": "searchDetailTable"}
    tables = soup.find_all("table", table_classes_filter)
    print(len(tables))

    sub_table_classes_filter = {"class": "subSearch"}
    sub_tables = soup.find_all("table", sub_table_classes_filter)
    print(len(sub_tables))

    if len(sub_tables) < 6:
        continue

    # *** 基本信息 *** #
    # print(tables[0])
    basic_tds = tables[0].find_all("td")
    print(len(basic_tds))

    # 登记号
    if basic_tds[0].contents:
        print(basic_tds[0].contents[0].strip())
        drug_trials_sheet["B" + str(row_index)] = basic_tds[0].contents[0].strip()

    # 试验状态
    if basic_tds[1].contents:
        print(basic_tds[1].contents[0].strip())
        drug_trials_sheet["C" + str(row_index)] = basic_tds[1].contents[0].strip()

    # 首次公示信息日期
    if basic_tds[3].contents:
        print(basic_tds[3].contents[0].strip())
        drug_trials_sheet["D" + str(row_index)] = basic_tds[3].contents[0].strip()

    # *** 题目和背景信息 *** #
    # print(tables[1])
    background_tds = tables[1].find_all("td")
    print(len(background_tds))

    # 其他相关登记号
    if background_tds[1].contents:
        print(background_tds[1].contents[0].strip())
        drug_trials_sheet["E" + str(row_index)] = background_tds[1].contents[0].strip()

    # 临床申请受理号
    if background_tds[4].contents:
        print(background_tds[4].contents[0].strip())
        drug_trials_sheet["G" + str(row_index)] = background_tds[4].contents[0].strip()

    # 药物名称
    if background_tds[2].contents:
        print(background_tds[2].contents[0].strip())
        drug_trials_sheet["H" + str(row_index)] = background_tds[2].contents[0].strip()

    # 药物类型
    if background_tds[3].contents:
        print(background_tds[3].contents[0].strip())
        drug_trials_sheet["I" + str(row_index)] = background_tds[3].contents[0].strip()

    # 适应症
    if background_tds[5].contents:
        print(background_tds[5].contents[0].strip())
        drug_trials_sheet["J" + str(row_index)] = background_tds[5].contents[0].strip()

    # 试验专业题目
    if background_tds[6].contents:
        print(background_tds[6].contents[0].strip())
        drug_trials_sheet["L" + str(row_index)] = background_tds[6].contents[0].strip()

    # 试验通俗题目
    if background_tds[7].contents:
        print(background_tds[7].contents[0].strip())
        drug_trials_sheet["M" + str(row_index)] = background_tds[7].contents[0].strip()

    # 试验方案编号
    if background_tds[8].contents:
        print(background_tds[8].contents[0].strip())
        drug_trials_sheet["O" + str(row_index)] = background_tds[8].contents[0].strip()

    # 方案最新版本号
    if background_tds[9].contents:
        print(background_tds[9].contents[0].strip())
        drug_trials_sheet["P" + str(row_index)] = background_tds[9].contents[0].strip()

    # 方案是否为联合用药
    if background_tds[11].contents:
        print(background_tds[11].contents[0].strip())
        drug_trials_sheet["Q" + str(row_index)] = background_tds[11].contents[0].strip()

    # 版本日期
    if background_tds[10].contents:
        print(background_tds[10].contents[0].strip())
        drug_trials_sheet["R" + str(row_index)] = background_tds[10].contents[0].strip()

    # *** 申请人信息 *** #
    # print(tables[2])
    applicant_tds = tables[2].find_all("td")
    print(len(applicant_tds))

    # 申请人名称
    applicant_inputs = applicant_tds[0].find_all("input")
    applicant = ""
    # print(applicant_inputs)
    for applicant_input in applicant_inputs:
        # print(applicant_input["value"])
        applicant = applicant + applicant_input["value"] + "\n"
    print(applicant)
    drug_trials_sheet["T" + str(row_index)] = applicant

    # 联系人姓名
    if applicant_tds[1].contents:
        print(applicant_tds[1].contents[0].strip())
        drug_trials_sheet["U" + str(row_index)] = applicant_tds[1].contents[0].strip()

    # 联系人座机
    if applicant_tds[2].contents:
        print(applicant_tds[2].contents[0].strip())
        drug_trials_sheet["V" + str(row_index)] = applicant_tds[2].contents[0].strip()

    # 联系人手机
    if applicant_tds[3].contents:
        print(applicant_tds[3].contents[0].strip())
        drug_trials_sheet["W" + str(row_index)] = applicant_tds[3].contents[0].strip()

    # 联系人邮箱
    if applicant_tds[4].contents:
        print(applicant_tds[4].contents[0].strip())
        drug_trials_sheet["X" + str(row_index)] = applicant_tds[4].contents[0].strip()

    # 联系人地址
    if applicant_tds[5].contents:
        print(applicant_tds[5].contents[0].strip())
        drug_trials_sheet["Y" + str(row_index)] = applicant_tds[5].contents[0].strip()

    # 联系人邮编
    if applicant_tds[6].contents:
        print(applicant_tds[6].contents[0].strip())
        drug_trials_sheet["Z" + str(row_index)] = applicant_tds[6].contents[0].strip()

    # *** 临床试验信息 *** #
    # print(tables[3])
    trial_tds = tables[3].find_all("td")
    print(len(trial_tds))

    # 试验目的
    if divs[0].next_sibling:
        print(divs[0].next_sibling.strip())
        drug_trials_sheet["AB" + str(row_index)] = divs[0].next_sibling.strip()

    # 试验分类
    if trial_tds[0].contents:
        print(trial_tds[0].contents[0].strip())
        drug_trials_sheet["AC" + str(row_index)] = trial_tds[0].contents[0].strip()

    # 试验分期
    if trial_tds[1].contents:
        print(trial_tds[1].contents[0].strip())
        drug_trials_sheet["AD" + str(row_index)] = trial_tds[1].contents[0].strip()

    # 试验范围
    if trial_tds[5].contents:
        print(trial_tds[5].contents[0].strip())
        drug_trials_sheet["AE" + str(row_index)] = trial_tds[5].contents[0].strip()

    # 设计类型
    if trial_tds[2].contents:
        print(trial_tds[2].contents[0].strip())
        drug_trials_sheet["AF" + str(row_index)] = trial_tds[2].contents[0].strip()

    # 随机化
    if trial_tds[3].contents:
        print(trial_tds[3].contents[0].strip())
        drug_trials_sheet["AG" + str(row_index)] = trial_tds[3].contents[0].strip()

    # 盲法
    if trial_tds[4].contents:
        print(trial_tds[4].contents[0].strip())
        drug_trials_sheet["AH" + str(row_index)] = trial_tds[4].contents[0].strip()

    # *** 受试者信息 *** #
    # print(tables[4])
    subject_tds = tables[4].find_all("td")
    print(len(subject_tds))

    # 年龄
    if subject_tds[0].contents:
        print(subject_tds[0].contents[0].strip())
        drug_trials_sheet["AJ" + str(row_index)] = subject_tds[0].contents[0].strip()

    # 性别
    if subject_tds[1].contents:
        print(subject_tds[1].contents[0].strip())
        drug_trials_sheet["AK" + str(row_index)] = subject_tds[1].contents[0].strip()

    # 健康受试者
    if subject_tds[2].contents:
        print(subject_tds[2].contents[0].strip())
        drug_trials_sheet["AL" + str(row_index)] = subject_tds[2].contents[0].strip()

    # *** 入选标准 *** #
    # print(sub_tables[0])
    selected_tds = sub_tables[0].find_all("td")
    print(len(selected_tds))

    selected_string = ""
    for selected_td in selected_tds:
        if selected_td.contents:
            selected_string = selected_string + selected_td.contents[0].strip() + "\n"
    print(selected_string)
    drug_trials_sheet["AM" + str(row_index)] = selected_string

    # *** 排除标准 *** #
    # print(sub_tables[1])
    eliminated_tds = sub_tables[1].find_all("td")
    print(len(eliminated_tds))

    eliminated_string = ""
    for eliminated_td in eliminated_tds:
        if eliminated_td.contents:
            eliminated_string = eliminated_string + eliminated_td.contents[0].strip() + "\n"
    print(eliminated_string)
    drug_trials_sheet["AN" + str(row_index)] = eliminated_string

    # *** 试验药 *** #
    # print(sub_tables[2])
    drug_tds = sub_tables[2].find_all("td")
    print(len(drug_tds))

    drug_string = ""
    for drug_td in drug_tds:
        for drug_content in drug_td.contents:
            if drug_content and str(drug_content).strip() != "<br/>":
                drug_string = drug_string + str(drug_content).strip() + "\n"
    print(drug_string)
    drug_trials_sheet["AQ" + str(row_index)] = drug_string

    # *** 对照药 *** #
    # print(sub_tables[3])
    control_tds = sub_tables[3].find_all("td")
    print(len(control_tds))

    control_string = ""
    for control_td in control_tds:
        for control_content in control_td.contents:
            if control_content and str(control_content).strip() != "<br/>":
                control_string = control_string + str(control_content).strip() + "\n"
    print(control_string)
    drug_trials_sheet["AR" + str(row_index)] = control_string

    # *** 主要终点指标 *** #
    # print(sub_tables[4])
    primary_endpoint_tds = sub_tables[4].find_all("td")
    print(len(primary_endpoint_tds))

    primary_endpoint_string = ""
    for primary_endpoint_td in primary_endpoint_tds:
        for primary_endpoint_content in primary_endpoint_td.contents:
            if primary_endpoint_content and str(primary_endpoint_content).strip() != "<br/>":
                primary_endpoint_string = primary_endpoint_string + str(primary_endpoint_content).strip() + "\n"
    print(primary_endpoint_string)
    drug_trials_sheet["AT" + str(row_index)] = primary_endpoint_string

    # *** 次要终点指标 *** #
    # print(sub_tables[5])
    secondary_endpoint_tds = sub_tables[5].find_all("td")
    print(len(secondary_endpoint_tds))

    secondary_endpoint_string = ""
    for secondary_endpoint_td in secondary_endpoint_tds:
        for secondary_endpoint_content in secondary_endpoint_td.contents:
            if secondary_endpoint_content and str(secondary_endpoint_content).strip() != "<br/>":
                secondary_endpoint_string = secondary_endpoint_string + str(secondary_endpoint_content).strip() + "\n"
    print(secondary_endpoint_string)
    drug_trials_sheet["AU" + str(row_index)] = secondary_endpoint_string

    # 数据安全检查委员会（DMC）
    if divs[5].next_sibling:
        print(divs[5].next_sibling.strip())
        drug_trials_sheet["AV" + str(row_index)] = divs[5].next_sibling.strip()

    # 为受试者购买试验伤害保险
    if divs[6].next_sibling:
        print(divs[6].next_sibling.strip())
        drug_trials_sheet["AO" + str(row_index)] = divs[6].next_sibling.strip()

    # 试验状态
    if divs[9].next_sibling:
        print(divs[9].next_sibling.strip())
        drug_trials_sheet["AX" + str(row_index)] = divs[9].next_sibling.strip()

    # *** 试验人数 *** #
    # print(tables[len(tables)-3])
    people_tds = tables[len(tables)-3].find_all("td")
    print(len(people_tds))

    # 目标入组人数
    if people_tds[0].contents:
        print(people_tds[0].contents[0].strip())
        drug_trials_sheet["AY" + str(row_index)] = people_tds[0].contents[0].strip()

    # 已经入组人数
    if people_tds[1].contents:
        print(people_tds[1].contents[0].strip())
        drug_trials_sheet["AZ" + str(row_index)] = people_tds[1].contents[0].strip()

    # 实际入组人数
    if people_tds[2].contents:
        print(people_tds[2].contents[0].strip())
        drug_trials_sheet["BA" + str(row_index)] = people_tds[2].contents[0].strip()

    # *** 受试者招募及试验完成日期 *** #
    # print(tables[len(tables)-2])
    date_tds = tables[len(tables)-2].find_all("td")
    print(len(date_tds))

    # 第一列受试者签署知情同意书日期
    if date_tds[0].contents:
        print(date_tds[0].contents[0].strip())
        drug_trials_sheet["BB" + str(row_index)] = date_tds[0].contents[0].strip()

    # 第一列受试者入组日期
    if date_tds[1].contents:
        print(date_tds[1].contents[0].strip())
        drug_trials_sheet["BC" + str(row_index)] = date_tds[1].contents[0].strip()

    # 试验完成日期
    if date_tds[2].contents:
        print(date_tds[2].contents[0].strip())
        drug_trials_sheet["BD" + str(row_index)] = date_tds[2].contents[0].strip()

    # *** 各参加机构信息 *** #
    # print(tables[len(tables)-5])
    institution_tds = tables[len(tables)-5].find_all("td")
    print(len(institution_tds))

    institution_string = ""
    for institution_td in institution_tds:
        if institution_td.contents:
            institution_string = institution_string + institution_td.contents[0].strip() + "\n"
    print(institution_string)
    drug_trials_sheet["BF" + str(row_index)] = institution_string

    # *** 伦理委员会信息 *** #
    # print(tables[len(tables)-4])
    committee_tds = tables[len(tables)-4].find_all("td")
    print(len(committee_tds))

    committee_string = ""
    for committee_td in committee_tds:
        if committee_td.contents:
            committee_string = committee_string + committee_td.contents[0].strip() + "\n"
    print(committee_string)
    drug_trials_sheet["BG" + str(row_index)] = committee_string

drug_trials_wb.save("drug_data/Generated - China Drug Trials.xlsx")