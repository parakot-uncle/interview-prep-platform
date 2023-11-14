function Card(props) {
  return (
    <div
      className={`rounded-lg p-4 ${props?.className}`}
      onClick={props?.onClick}
      style={{
        ...(props?.backgroundColor && {
          backgroundColor: props?.backgroundColor,
        }),
      }}
    >
      {props?.children}
    </div>
  );
}

export default Card;
