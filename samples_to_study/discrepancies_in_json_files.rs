// 이 코드는 serde_json 라이브러리를 사용하여 JSON 파일을 불러온 후, JSON 값들을 비교하여 차이점을 찾습니다. compare_json_values() 함수는 재귀적으로 객체와 배열을 탐색하면서 값들을 비교하며, 차이점을 발견하면 경로와 함께 결과 벡터에 추가합니다. 마지막으로, 결과 벡터를 출력합니다. 이 코드를 실행하면 두 JSON 파일 간의 차이점을 쉽게 확인할 수 있습니다.


use serde_json::{Result, Value};
use std::fs;

fn main() -> Result<()> {
    // 첫 번째 JSON 파일 불러오기
    let json1 = fs::read_to_string("file1.json")?;
    let obj1: Value = serde_json::from_str(&json1)?;

    // 두 번째 JSON 파일 불러오기
    let json2 = fs::read_to_string("file2.json")?;
    let obj2: Value = serde_json::from_str(&json2)?;

    // 두 객체를 비교하여 차이점 찾기
    let mut result = Vec::new();
    compare_json_values(&mut result, "", &obj1, &obj2);

    // 차이점 출력
    for r in result {
        println!("{}", r);
    }

    Ok(())
}

fn compare_json_values(result: &mut Vec<String>, path: &str, value1: &Value, value2: &Value) {
    match (value1, value2) {
        (Value::Object(obj1), Value::Object(obj2)) => {
            for (k, v1) in obj1.iter() {
                let v2 = obj2.get(k);
                let new_path = format!("{}{}", path, k);
                compare_json_values(result, &new_path, v1, v2.unwrap_or(&Value::Null));
            }
        }
        (Value::Array(arr1), Value::Array(arr2)) => {
            for (i, v1) in arr1.iter().enumerate() {
                let v2 = arr2.get(i);
                let new_path = format!("{}[{}]", path, i);
                compare_json_values(result, &new_path, v1, v2.unwrap_or(&Value::Null));
            }
        }
        _ => {
            if value1 != value2 {
                let msg = format!("{}: {} != {}", path, value1, value2);
                result.push(msg);
            }
        }
    }
}
